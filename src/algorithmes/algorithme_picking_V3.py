# algorithmes/algorithme_picking.py

from models.colis import Colis
from models.chariot import Chariot
from models.tournee import Tournee
from collections import defaultdict
import numpy as np
from sklearn.cluster import KMeans
import logging
logger = logging.getLogger(__name__)

def repartition_articles_colis(entrepot):
    """
    Répartit les articles des commandes dans les colis en optimisant les localisations pour réduire les distances.

    :param entrepot: Objet Entrepot contenant les commandes et les produits.
    :return: Liste des colis créés.
    """
    colis_list = []
    id_colis = 1

    for commande in entrepot.commandes.values():
        # Créer un dictionnaire des produits par localisation
        produits_par_localisation = defaultdict(list)
        for id_produit, quantite in commande.lignes_commande.items():
            produit = entrepot.produits[id_produit]
            produits_par_localisation[produit.localisation].append((id_produit, quantite, produit))

        # Trier les localisations (vous pouvez choisir un autre critère de tri)
        localisations_triees = sorted(produits_par_localisation.keys())

        # Liste des colis pour cette commande
        colis_commande = []
        colis = Colis(id_colis, commande.id, entrepot.capacite_colis[0], entrepot.capacite_colis[1])
        id_colis += 1
        colis_commande.append(colis)

        # Répartir les produits dans les colis en groupant par localisation
        for localisation in localisations_triees:
            produits = produits_par_localisation[localisation]
            for id_produit, quantite, produit in produits:
                quantite_restante = quantite

                while quantite_restante > 0:
                    quantite_ajoutee = colis.peut_ajouter_produit(produit, quantite_restante)
                    if quantite_ajoutee > 0:
                        colis.ajouter_produit(produit, quantite_ajoutee)
                        quantite_restante -= quantite_ajoutee
                    else:
                        # Si le colis est plein, créer un nouveau colis
                        colis = Colis(id_colis, commande.id, entrepot.capacite_colis[0], entrepot.capacite_colis[1])
                        id_colis += 1
                        colis_commande.append(colis)

        # Ajouter les colis non vides à la liste générale
        colis_non_vides = [colis for colis in colis_commande if colis.produits]
        colis_list.extend(colis_non_vides)

    return colis_list

def regroupement_colis_chariots(entrepot, colis_list):
    """
    Regroupe les colis sur les chariots en utilisant le clustering pour minimiser les distances.

    :param entrepot: Objet Entrepot.
    :param colis_list: Liste des colis à affecter aux chariots.
    :return: Liste des chariots créés.
    """
    from sklearn.cluster import KMeans
    import numpy as np
    from collections import defaultdict

    capacite_chariot = entrepot.capacite_chariot

    # Calculer les centres de gravité des colis en utilisant les positions des produits
    positions = []
    for colis in colis_list:
        coordonnees_produits = []
        for id_produit in colis.produits:
            produit = entrepot.produits[id_produit]
            location = entrepot.graphe.locations[produit.localisation]
            coordonnees_produits.append([location.x, location.y])
        # Calculer le centre de gravité du colis
        centre = np.mean(coordonnees_produits, axis=0)
        positions.append(centre)

    # Déterminer le nombre de clusters (chariots) nécessaires
    nb_chariots = max(1, len(colis_list) // capacite_chariot)

    # Fixer la graine aléatoire pour KMeans
    random_state = 42

    # Appliquer le clustering
    if len(positions) < nb_chariots:
        nb_chariots = len(positions)
    if nb_chariots == 0:
        nb_chariots = 1
    kmeans = KMeans(n_clusters=nb_chariots, random_state=random_state)
    positions = np.array(positions)
    labels = kmeans.fit_predict(positions)

    chariots = []
    id_chariot = 1

    # Créer un dictionnaire pour regrouper les colis par cluster
    colis_par_cluster = defaultdict(list)
    for label, colis in zip(labels, colis_list):
        colis_par_cluster[label].append(colis)

    # Créer les chariots en respectant la capacité
    for colis_cluster in colis_par_cluster.values():
        for i in range(0, len(colis_cluster), capacite_chariot):
            chariot = Chariot(id_chariot, capacite_chariot)
            for colis in colis_cluster[i:i + capacite_chariot]:
                chariot.ajouter_colis(colis)
            chariots.append(chariot)
            id_chariot += 1

    return chariots

def calcul_tournees(entrepot, chariots):
    """
    Calcule les tournées pour chaque chariot en optimisant le parcours des positions.

    :param entrepot: Objet Entrepot.
    :param chariots: Liste des chariots.
    :return: Liste des tournées.
    """
    tournees = []
    id_tournee = 1

    for chariot in chariots:
        tournee = Tournee(id_tournee, chariot)
        positions_a_visiter = []

        for colis in chariot.colis:
            for id_produit in colis.produits:
                produit = entrepot.produits[id_produit]
                id_localisation = produit.localisation
                if id_localisation not in positions_a_visiter:
                    positions_a_visiter.append(id_localisation)

        # Ajouter le dépôt de départ au début et le dépôt d'arrivée à la fin
        positions_a_visiter = [entrepot.graphe.depot_depart] + positions_a_visiter + [entrepot.graphe.depot_arrivee]

        # Optimiser la séquence des positions
        sequence_positions = optimiser_parcours(positions_a_visiter, entrepot)

        tournee.sequence_positions = sequence_positions

        # Calculer la distance totale en utilisant le graphe
        distance_totale = 0
        for i in range(len(sequence_positions) - 1):
            depart = sequence_positions[i]
            arrivee = sequence_positions[i + 1]
            distance = entrepot.graphe.shortest_path_length(depart, arrivee)
            distance_totale += distance

        tournee.distance_totale = distance_totale

        tournees.append(tournee)
        id_tournee += 1

    return tournees

def optimiser_parcours(positions, entrepot):
    """
    Optimise le parcours des positions en utilisant le graphe de l'entrepôt
    et l'algorithme 2-opt.

    :param positions: Liste des positions (id_localisation) à visiter.
    :param entrepot: Objet Entrepot contenant le graphe de l'entrepôt.
    :return: Liste ordonnée des positions optimisées.
    """
    if not positions:
        return []

    graphe = entrepot.graphe

    # Assurer que les plus courts chemins sont calculés
    if not hasattr(graphe, 'all_pairs_distances'):
        graphe.calculer_tous_plus_courts_chemins()

    # Construire la matrice des distances pour les positions données
    distance_matrix = {}
    for i in positions:
        distance_matrix[i] = {}
        for j in positions:
            distance_matrix[i][j] = graphe.shortest_path_length(i, j)

    # Générer une route initiale avec l'heuristique du plus proche voisin
    route = nearest_neighbor_route(positions, distance_matrix)

    # Améliorer la route avec l'algorithme 2-opt
    optimized_route = two_opt(route, distance_matrix)

    return optimized_route

def nearest_neighbor_route(positions, distance_matrix):
    """
    Génère une route initiale en utilisant l'heuristique du plus proche voisin.

    :param positions: Liste des positions (id_localisation) à visiter.
    :param distance_matrix: Matrice des distances entre les positions.
    :return: Liste ordonnée des positions.
    """
    positions = positions[:]
    route = [positions.pop(0)]  # Commencez par le premier point
    while positions:
        last = route[-1]
        next_pos = min(positions, key=lambda x: distance_matrix[last][x])
        positions.remove(next_pos)
        route.append(next_pos)
    return route

def two_opt(route, distance_matrix):
    """
    Améliore une route en utilisant l'algorithme 2-opt.

    :param route: Liste ordonnée des positions (identifiants de localisations).
    :param distance_matrix: Matrice des distances entre les positions.
    :return: Nouvelle route optimisée.
    """
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue  # Échanges adjacents inutiles
                new_route = route[:]
                # Inverser le segment entre i et j
                new_route[i:j] = route[j - 1:i - 1:-1]
                new_distance = calculer_distance_totale(new_route, distance_matrix)
                best_distance = calculer_distance_totale(best, distance_matrix)
                if new_distance < best_distance:
                    best = new_route
                    improved = True
        route = best
    return best

def calculer_distance_totale(route, distance_matrix):
    """
    Calcule la distance totale d'une route donnée.

    :param route: Liste ordonnée des positions.
    :param distance_matrix: Matrice des distances entre les positions.
    :return: Distance totale.
    """
    distance_totale = 0
    for i in range(len(route) - 1):
        distance_totale += distance_matrix[route[i]][route[i + 1]]
    return distance_totale
