# algorithmes/algorithme_picking.py
from models.colis import Colis
from models.chariot import Chariot
from models.tournee import Tournee
import logging
logger = logging.getLogger(__name__)
def repartition_articles_colis(entrepot):
    """
    Répartit les articles des commandes dans les colis en respectant les contraintes.
    :param entrepot: Objet Entrepot contenant les commandes et les produits.
    :return: Liste des colis créés.
    """
    colis_list = []
    id_colis = 1
    for commande in entrepot.commandes.values():
        produits_commande = list(commande.lignes_commande.items())
        # Trier les produits par volume décroissant
        produits_commande.sort(key=lambda x: entrepot.produits[x[0]].volume_unitaire, reverse=True)
        # Liste des colis pour cette commande
        colis_commande = []
        for _ in range(commande.mc):
            colis = Colis(id_colis, commande.id, entrepot.capacite_colis[0], entrepot.capacite_colis[1])
            id_colis += 1
            colis_commande.append(colis)
        for id_produit, quantite in produits_commande:
            produit = entrepot.produits[id_produit]
            quantite_restante = quantite
            # Vérifier si le produit peut être ajouté à un colis (si son poids/volume unitaire <= capacité)
            if (produit.poids_unitaire > colis.poids_max) or (produit.volume_unitaire > colis.volume_max):
                logger.error(f"Le produit {id_produit} de la commande {commande.id} ne peut pas être ajouté à un colis (poids ou volume unitaire trop grand)")
                continue
            # Tenter d'ajouter le produit dans les colis existants
            for colis in colis_commande:
                quantite_ajoutee = colis.peut_ajouter_produit(produit, quantite_restante)
                if quantite_ajoutee > 0:
                    colis.ajouter_produit(produit, quantite_ajoutee)
                    quantite_restante -= quantite_ajoutee
                if quantite_restante == 0:
                    break
            # Si quantite_restante > 0, on ne peut pas ajouter le produit dans les colis existants
            if quantite_restante > 0:
                logger.warning(f"Impossible d'ajouter la quantité {quantite_restante} du produit {id_produit} dans les colis de la commande {commande.id}")
        # Ajouter les colis non vides à la liste générale
        colis_non_vides = [colis for colis in colis_commande if colis.produits]
        colis_list.extend(colis_non_vides)
    return colis_list
def regroupement_colis_chariots(entrepot, colis_list):
    """
    Regroupe les colis sur les chariots en respectant la capacité maximale K.
    :param entrepot: Objet Entrepot.
    :param colis_list: Liste des colis à affecter aux chariots.
    :return: Liste des chariots créés.
    """
    chariots = []
    id_chariot = 1
    capacite_chariot = entrepot.capacite_chariot
    # Trier les colis par ID de localisation minimum des produits qu'ils contiennent
    colis_list.sort(key=lambda c: min([entrepot.produits[pid].localisation for pid in c.produits]))
    for i in range(0, len(colis_list), capacite_chariot):
        chariot = Chariot(id_chariot, capacite_chariot)
        for colis in colis_list[i:i+capacite_chariot]:
            chariot.ajouter_colis(colis)
        chariots.append(chariot)
        id_chariot += 1
    return chariots
def calcul_tournees(entrepot, chariots):
    """
    Calcule les tournées pour chaque chariot.
    :param entrepot: Objet Entrepot.
    :param chariots: Liste des chariots.
    :return: Liste des tournées.
    """
    tournees = []
    id_tournee = 1
    for chariot in chariots:
        tournee = Tournee(id_tournee, chariot)
        # Calculer la séquence des positions à visiter
        positions_a_visiter = set()
        for colis in chariot.colis:
            for id_produit in colis.produits:
                produit = entrepot.produits[id_produit]
                positions_a_visiter.add(produit.localisation)
        # Convertir en liste et trier selon le sens de parcours imposé
        sequence_positions = sorted(positions_a_visiter)
        tournee.sequence_positions = sequence_positions
        # Calculer la distance totale (simplifié ici)
        tournee.distance_totale = len(sequence_positions)  # Simplification
        tournees.append(tournee)
        id_tournee += 1
    return tournees