# analyseur_instances.py

import logging
from models.produit import Produit
from models.commande import Commande
from models.entrepot import Entrepot
from models.graphe_entrepot import GrapheEntrepot

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def analyser_instance(chemin_fichier):
    """
    Analyse un fichier d'instance et retourne un objet Entrepot rempli.

    :param chemin_fichier: Chemin vers le fichier d'instance.
    :return: Objet Entrepot.
    """
    logging.info(f"Analyse du fichier d'instance: {chemin_fichier}")
    entrepot = Entrepot()
    graphe = GrapheEntrepot()
    try:
        with open(chemin_fichier, 'r') as fichier:
            lignes = fichier.readlines()
    except FileNotFoundError:
        logging.error(f"Le fichier {chemin_fichier} n'a pas été trouvé.")
        return None

    i = 0
    nb_produits = 0
    nb_commandes = 0
    while i < len(lignes):
        ligne = lignes[i].strip()

        # Vérifier les mots-clés même si la ligne commence par '//'
        if 'NbLocations' in ligne:
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            nb_locations = int(lignes[i].strip())
            logging.info(f"NbLocations: {nb_locations}")
            i += 1

        elif 'NbProducts' in ligne:
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            nb_produits = int(lignes[i].strip())
            logging.info(f"NbProducts: {nb_produits}")
            i += 1

        elif 'K: NbBoxesTrolley' in ligne:
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            CAPACITE_CHARIOT = int(lignes[i].strip())
            entrepot.capacite_chariot = CAPACITE_CHARIOT
            logging.info(f"CAPACITE_CHARIOT: {CAPACITE_CHARIOT}")
            i += 1

        elif 'NbDimensionsCapacity' in ligne:
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            nb_dimensions = int(lignes[i].strip())
            logging.info(f"NbDimensionsCapacity: {nb_dimensions}")
            i += 1

        elif 'B: CapaBox' in ligne:
            i += 1
            # Sauter les commentaires et les lignes vides
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            capacites = lignes[i].strip().split()
            poids_max = float(capacites[0])
            volume_max = float(capacites[1])
            entrepot.capacite_colis = (poids_max, volume_max)
            logging.info(f"CAPACITE_COLIS: {entrepot.capacite_colis}")
            i += 1

        # Lorsque vous lisez 'K: NbBoxOnCart'
        elif 'K: NbBoxOnCart' in ligne:
            i += 1
            # Sauter les commentaires et les lignes vides
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            entrepot.capacite_chariot = int(lignes[i].strip())
            logging.info(f"CAPACITE_CHARIOT: {entrepot.capacite_chariot}")
            i += 1

        elif 'A box can accept mixed orders' in ligne:
            i += 1

        elif 'Products' in ligne:
            i += 1  # Sauter la ligne actuelle
            # Sauter les lignes de commentaires
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            # Lecture des produits
            produits_lus = 0
            logging.info("Début de la lecture des produits")
            while produits_lus < nb_produits and i < len(lignes):
                ligne_produit = lignes[i].strip()
                if not ligne_produit or ligne_produit.startswith('//'):
                    i += 1
                    continue
                data = ligne_produit.split()
                if len(data) >= 4:
                    try:
                        id_produit = int(data[0])
                        id_localisation = int(data[1])
                        poids_unitaire = float(data[2])
                        volume_unitaire = float(data[3])
                        logging.debug(f"Produit {id_produit}: poids_unitaire={poids_unitaire}, volume_unitaire={volume_unitaire}")
                        produit = Produit(id_produit, id_localisation, poids_unitaire, volume_unitaire)
                        entrepot.ajouter_produit(produit)
                        logging.debug(f"Produit ajouté: {produit}")
                        produits_lus += 1
                    except ValueError as e:
                        logging.error(f"Erreur de conversion à la ligne {i}: {e}")
                else:
                    logging.warning(f"Ligne produit invalide à la ligne {i}: {ligne_produit}")
                i += 1

        elif 'Orders' in ligne:
            i += 1  # Sauter la ligne actuelle
            # Sauter les lignes de commentaires
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            # Lire NbOrders
            nb_commandes = int(lignes[i].strip())
            logging.info(f"NbOrders: {nb_commandes}")
            i += 1
            # Sauter les lignes de commentaires
            while i < len(lignes) and (lignes[i].strip().startswith('//') or not lignes[i].strip()):
                i += 1
            # Lecture des commandes
            commandes_lues = 0
            logging.info("Début de la lecture des commandes")
            while commandes_lues < nb_commandes and i < len(lignes):
                ligne_commande = lignes[i].strip()
                if not ligne_commande or ligne_commande.startswith('//'):
                    i += 1
                    continue
                data = ligne_commande.split()
                if len(data) >= 3:
                    id_commande = int(data[0])
                    mc = int(data[1])
                    nb_prod_in_order = int(data[2])
                    commande = Commande(id_commande, mc)
                    idx = 3  # Index pour les paires produit-quantité
                    while idx < len(data):
                        if idx + 1 >= len(data):
                            logging.warning(f"Données incomplètes pour la commande {id_commande} à la ligne {i}")
                            break
                        id_produit = int(data[idx])
                        quantite = int(data[idx + 1])
                        commande.ajouter_produit(id_produit, quantite)
                        idx += 2
                    entrepot.ajouter_commande(commande)
                    logging.debug(f"Commande ajoutée: {commande}")
                    commandes_lues += 1
                    i += 1
                else:
                    logging.warning(f"Ligne commande invalide à la ligne {i}: {ligne_commande}")
                    i += 1

        elif 'Graph' in ligne:
            i += 1  # Sauter la ligne actuelle
            logging.info("Début de la lecture du graphe")
            # Implémentation de la lecture du graphe (vous pouvez compléter ici)
            break  # Pour cet exemple, nous sortons de la boucle principale

        else:
            # Ignorer les lignes de commentaires et les lignes vides
            if ligne.startswith('//') or not ligne:
                i += 1
                continue

            # Sinon, ligne non reconnue
            i += 1  # Incrémenter pour éviter une boucle infinie

    # Assigner le graphe à l'entrepôt
    entrepot.definir_graphe(graphe)
    logging.info(f"Fin de l'analyse du fichier. Produits lus: {len(entrepot.produits)}, Commandes lues: {len(entrepot.commandes)}")
    return entrepot
