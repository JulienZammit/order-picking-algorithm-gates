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

    # Appliquer le clustering
    if len(positions) < nb_chariots:
        nb_chariots = len(positions)
    if nb_chariots == 0:
        nb_chariots = 1
    kmeans = KMeans(n_clusters=nb_chariots)
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
    Optimise le parcours des positions en utilisant le graphe de l'entrepôt.

    :param positions: Liste des positions (id_localisation) à visiter.
    :param entrepot: Objet Entrepot contenant le graphe de l'entrepôt.
    :return: Liste ordonnée des positions optimisées.
    """
    if not positions:
        return []

    graphe = entrepot.graphe

    # Calculer la matrice des distances entre les positions en utilisant les plus courts chemins
    n = len(positions)
    distance_matrix = [[0]*n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                distance_matrix[i][j] = 0
            else:
                distance = graphe.shortest_path_length(positions[i], positions[j]) or float('inf')
                distance_matrix[i][j] = distance

    # Appliquer l'heuristique du plus proche voisin en utilisant la matrice des distances
    visited = [False] * n
    sequence = []
    current_index = 0  # On commence par la première position
    sequence.append(positions[current_index])
    visited[current_index] = True

    for _ in range(n - 1):
        min_distance = float('inf')
        next_index = None
        for j in range(n):
            if not visited[j] and distance_matrix[current_index][j] < min_distance:
                min_distance = distance_matrix[current_index][j]
                next_index = j
        if next_index is not None:
            sequence.append(positions[next_index])
            visited[next_index] = True
            current_index = next_index
        else:
            break  # Plus de positions à visiter

    return sequence
