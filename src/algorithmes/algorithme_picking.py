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
    Répartit les articles des commandes dans les colis en optimisant le remplissage des colis.
    Utilise l'algorithme First-Fit Decreasing pour le bin packing.

    :param entrepot: Objet Entrepot contenant les commandes et les produits.
    :return: Liste des colis créés.
    """
    colis_list = []
    id_colis = 1

    for commande in entrepot.commandes.values():
        produits_commande = []

        # Construire une liste des produits avec quantités
        for id_produit, quantite in commande.lignes_commande.items():
            produit = entrepot.produits[id_produit]
            volume_total = produit.volume_unitaire * quantite
            poids_total = produit.poids_unitaire * quantite
            produits_commande.append({
                'id_produit': id_produit,
                'quantite': quantite,
                'produit': produit,
                'volume_total': volume_total,
                'poids_total': poids_total
            })

        # Trier les produits par volume total décroissant
        produits_tries = sorted(produits_commande, key=lambda x: x['volume_total'], reverse=True)

        # Liste des colis pour cette commande
        colis_commande = []

        for item in produits_tries:
            id_produit = item['id_produit']
            quantite = item['quantite']
            produit = item['produit']
            quantite_restante = quantite

            while quantite_restante > 0:
                # Tenter d'ajouter le produit dans les colis existants
                place_trouvee = False
                for colis in colis_commande:
                    quantite_ajoutee = colis.peut_ajouter_produit(produit, quantite_restante)
                    if quantite_ajoutee > 0:
                        colis.ajouter_produit(produit, quantite_ajoutee)
                        quantite_restante -= quantite_ajoutee
                        place_trouvee = True
                        if quantite_restante == 0:
                            break
                # Si le produit n'a pas pu être ajouté, créer un nouveau colis
                if not place_trouvee:
                    colis = Colis(id_colis, commande.id, entrepot.capacite_colis[0], entrepot.capacite_colis[1])
                    quantite_ajoutee = colis.peut_ajouter_produit(produit, quantite_restante)
                    if quantite_ajoutee > 0:
                        colis.ajouter_produit(produit, quantite_ajoutee)
                        quantite_restante -= quantite_ajoutee
                        colis_commande.append(colis)
                        id_colis += 1
                    else:
                        logger.warning(f"Le produit {id_produit} ne peut pas être ajouté dans un nouveau colis (trop volumineux).")
                        break  # Ou gérer autrement si le produit ne rentre pas dans un colis vide

        # Ajouter les colis non vides à la liste générale
        colis_list.extend(colis_commande)

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

    # Calculer les centres de gravité des colis
    positions = np.array([colis.centre_gravite(entrepot) for colis in colis_list])

    # Déterminer le nombre de clusters (chariots) nécessaires
    nb_chariots = max(1, len(colis_list) // capacite_chariot)

    # Appliquer le clustering
    if len(positions) < nb_chariots:
        nb_chariots = len(positions)
    if nb_chariots == 0:
        nb_chariots = 1
    kmeans = KMeans(n_clusters=nb_chariots)
    positions = positions.reshape(-1, 1) if positions.ndim == 1 else positions
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
            for colis in colis_cluster[i:i+capacite_chariot]:
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
    from scipy.spatial.distance import cdist
    import numpy as np

    tournees = []
    id_tournee = 1

    for chariot in chariots:
        tournee = Tournee(id_tournee, chariot)
        positions_a_visiter = []

        for colis in chariot.colis:
            for id_produit in colis.produits:
                produit = entrepot.produits[id_produit]
                if produit.localisation not in positions_a_visiter:
                    positions_a_visiter.append(produit.localisation)

        # Optimiser la séquence des positions
        sequence_positions = optimiser_parcours(positions_a_visiter, entrepot)

        tournee.sequence_positions = sequence_positions
        # Calculer la distance totale (simplifié ici)
        tournee.distance_totale = len(sequence_positions)  # Vous pouvez améliorer le calcul réel de la distance

        tournees.append(tournee)
        id_tournee += 1

    return tournees

def optimiser_parcours(positions, entrepot):
    """
    Implémente une heuristique du plus proche voisin pour optimiser le parcours des positions.

    :param positions: Liste des positions (id_localisation) à visiter.
    :param entrepot: Objet Entrepot contenant les localisations avec leurs coordonnées.
    :return: Liste ordonnée des positions optimisées.
    """
    import numpy as np

    if not positions:
        return []

    # Récupérer les coordonnées des positions
    coordonnees_positions = []
    for id_localisation in positions:
        if id_localisation in entrepot.localisations:
            x, y = entrepot.localisations[id_localisation][:2]
            coordonnees_positions.append((id_localisation, x, y))
        else:
            # Gestion du cas où la localisation n'est pas trouvée
            logger.warning(f"Localisation {id_localisation} non trouvée dans l'entrepôt.")
            coordonnees_positions.append((id_localisation, 0, 0))  # Coordonnées par défaut

    # Convertir en numpy array
    ids = [item[0] for item in coordonnees_positions]
    coords = np.array([[item[1], item[2]] for item in coordonnees_positions])

    n = len(coords)
    visited = [False] * n
    sequence = []
    current_index = 0  # On commence par la première position
    sequence.append(ids[current_index])
    visited[current_index] = True

    for _ in range(n - 1):
        distances = np.linalg.norm(coords - coords[current_index], axis=1)
        distances[visited] = np.inf  # Ignorer les positions déjà visitées
        next_index = np.argmin(distances)
        sequence.append(ids[next_index])
        visited[next_index] = True
        current_index = next_index

    return sequence