# analyseur_instances.py

import logging
import re
from models.produit import Produit
from models.commande import Commande
from models.entrepot import Entrepot
from models.graphe_entrepot import GrapheEntrepot
from models.location import Location
from models.arc import Arc

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def nettoyer_ligne_graph(lignes):
    """
    Supprime tout texte après le mot 'Graph' sur une ligne donnée.

    :param lignes: Liste des lignes du fichier.
    :return: Liste des lignes modifiées.
    """
    lignes_modifiees = []
    for ligne in lignes:
        if "Graph" in ligne:
            # Ne garder que la partie avant le mot 'Graph' et ajouter 'Graph'
            index = ligne.index("Graph")
            nouvelle_ligne = ligne[:index + len("Graph")] + "\n"
            lignes_modifiees.append(nouvelle_ligne)
        else:
            lignes_modifiees.append(ligne)
    return lignes_modifiees


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
    
    # TODO : supprimer tout ce qu'il y a derrière Graph
    # Nettoyage des lignes contenant 'Graph'
    lignes = nettoyer_ligne_graph(lignes)

    i = 0
    nb_produits = 0
    nb_commandes = 0
    while i < len(lignes):
        ligne = lignes[i].strip()

        # Supprimer les commentaires au début de la ligne
        ligne_sans_commentaire = re.sub(r'^//\s*', '', ligne)

        # Vérifier les mots-clés même si la ligne commence par '//' ou contient du texte supplémentaire
        if re.search(r'\bNbLocations\b', ligne_sans_commentaire):
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
                i += 1
            nb_locations = int(lignes[i].strip())
            logging.info(f"NbLocations: {nb_locations}")
            i += 1

        elif re.search(r'\bNbProducts\b', ligne_sans_commentaire):
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
                i += 1
            nb_produits = int(lignes[i].strip())
            logging.info(f"NbProducts: {nb_produits}")
            i += 1

        elif re.search(r'\bK: NbBoxesTrolley\b', ligne_sans_commentaire):
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
                i += 1
            CAPACITE_CHARIOT = int(lignes[i].strip())
            entrepot.capacite_chariot = CAPACITE_CHARIOT
            logging.info(f"CAPACITE_CHARIOT: {CAPACITE_CHARIOT}")
            i += 1

        elif re.search(r'\bNbDimensionsCapacity\b', ligne_sans_commentaire):
            i += 1
            # Skip comments and empty lines
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
                i += 1
            nb_dimensions = int(lignes[i].strip())
            logging.info(f"NbDimensionsCapacity: {nb_dimensions}")
            i += 1

        elif re.search(r'\bB: CapaBox\b', ligne_sans_commentaire):
            i += 1
            # Sauter les commentaires et les lignes vides
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
                i += 1
            capacites = lignes[i].strip().split()
            poids_max = float(capacites[0])
            volume_max = float(capacites[1])
            entrepot.capacite_colis = (poids_max, volume_max)
            logging.info(f"CAPACITE_COLIS: {entrepot.capacite_colis}")
            i += 1

        elif re.search(r'\bK: NbBoxOnCart\b', ligne_sans_commentaire):
            i += 1
            # Sauter les commentaires et les lignes vides
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
                i += 1
            entrepot.capacite_chariot = int(lignes[i].strip())
            logging.info(f"CAPACITE_CHARIOT: {entrepot.capacite_chariot}")
            i += 1

        elif re.search(r'\bA box can accept mixed orders\b', ligne_sans_commentaire):
            i += 1

        elif re.search(r'\bProducts\b', ligne_sans_commentaire):
            i += 1  # Sauter la ligne actuelle
            # Sauter les lignes de commentaires
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
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

        elif re.search(r'\bOrders\b', ligne_sans_commentaire):
            i += 1  # Sauter la ligne actuelle
            # Sauter les lignes de commentaires
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
                i += 1
            # Lire NbOrders
            nb_commandes = int(lignes[i].strip())
            logging.info(f"NbOrders: {nb_commandes}")
            i += 1
            # Sauter les lignes de commentaires
            while i < len(lignes) and (re.match(r'^\s*//', lignes[i]) or not lignes[i].strip()):
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
                        # Récupérer les coordonnées du produit depuis entrepot.produits
                        if id_produit in entrepot.produits:
                            coordonnees = entrepot.produits[id_produit].coordonnees
                        else:
                            logging.warning(f"Produit {id_produit} non trouvé pour la commande {id_commande}")
                            coordonnees = None
                        commande.ajouter_produit(id_produit, quantite, coordonnees)
                        idx += 2
                    entrepot.ajouter_commande(commande)
                    logging.debug(f"Commande ajoutée: {commande}")
                    commandes_lues += 1
                    i += 1
                else:
                    logging.warning(f"Ligne commande invalide à la ligne {i}: {ligne_commande}")
                    i += 1

        elif re.search(r'\bGraph\b', ligne_sans_commentaire):
            i += 1  # Passer à la ligne suivante
            logging.info("Début de la lecture du graphe")
            # Flags pour savoir dans quelle section nous sommes
            in_arcs_section = False
            in_locations_section = False
            while i < len(lignes):
                ligne = lignes[i].strip()
                ligne_sans_commentaire = re.sub(r'^//\s*', '', ligne)
                if not ligne_sans_commentaire:
                    i += 1
                    continue
                if re.search(r'\bArcs\b', ligne_sans_commentaire):
                    logging.info("Lecture des arcs")
                    in_arcs_section = True
                    in_locations_section = False
                    i += 1  # Passer à la ligne suivante
                    continue
                elif re.search(r'\bLocation coordinates\b', ligne_sans_commentaire):
                    logging.info("Lecture des localisations")
                    in_arcs_section = False
                    in_locations_section = True
                    i += 1  # Passer à la ligne suivante
                    continue
                elif re.search(r'\bNbVerticesIntersections\b', ligne_sans_commentaire):
                    i += 1
                    # Skip comments and empty lines
                    while i < len(lignes) and (not lignes[i].strip() or re.match(r'^\s*//', lignes[i])):
                        i += 1
                    if i < len(lignes):
                        nb_vertices = int(lignes[i].strip())
                        logging.info(f"NbVerticesIntersections: {nb_vertices}")
                        i += 1
                    continue
                elif re.search(r'\bDepartingDepot\b', ligne_sans_commentaire):
                    i += 1
                    # Skip comments and empty lines
                    while i < len(lignes) and (not lignes[i].strip() or re.match(r'^\s*//', lignes[i])):
                        i += 1
                    if i < len(lignes):
                        graphe.depot_depart = int(lignes[i].strip())
                        logging.info(f"Départ du dépôt: {graphe.depot_depart}")
                        i += 1
                    continue
                elif re.search(r'\bArrivalDepot\b', ligne_sans_commentaire):
                    i += 1
                    # Skip comments and empty lines
                    while i < len(lignes) and (not lignes[i].strip() or re.match(r'^\s*//', lignes[i])):
                        i += 1
                    if i < len(lignes):
                        graphe.depot_arrivee = int(lignes[i].strip())
                        logging.info(f"Arrivée au dépôt: {graphe.depot_arrivee}")
                        i += 1
                    continue
                elif in_arcs_section:
                    # Lecture des arcs
                    if ligne.startswith('//') or not ligne:
                        i += 1
                        continue
                    data = ligne.split()
                    if len(data) >= 3:
                        try:
                            start = int(data[0])
                            end = int(data[1])
                            distance = float(data[2])
                            arc = Arc(start, end, distance)
                            graphe.ajouter_arc(arc)
                            logging.debug(f"Arc ajouté: {arc}")
                        except ValueError as e:
                            logging.error(f"Erreur de conversion de l'arc à la ligne {i}: {e}")
                    else:
                        logging.warning(f"Ligne arc invalide à la ligne {i}: {ligne}")
                    i += 1
                elif in_locations_section:
                    # Lecture des localisations
                    if ligne.startswith('//') or not ligne:
                        i += 1
                        continue
                    data = ligne.split()
                    if len(data) >= 4:
                        try:
                            id_location = int(data[0])
                            x = float(data[1])
                            y = float(data[2])
                            # Le nom peut contenir des espaces, on le recompose
                            name = ' '.join(data[3:]).strip('"')
                            location = Location(id_location, x, y, name)
                            graphe.ajouter_location(location)
                            logging.debug(f"Location ajoutée: {location}")
                        except ValueError as e:
                            logging.error(f"Erreur de conversion de la localisation à la ligne {i}: {e}")
                    else:
                        logging.warning(f"Ligne localisation invalide à la ligne {i}: {ligne}")
                    i += 1
                else:
                    i += 1  # Incrémenter si aucune condition n'est remplie
            # Fin de la lecture du graphe
            logging.info("Fin de la lecture du graphe")
            break  # Sortir de la boucle principale après avoir lu le graphe

        else:
            i += 1  # Incrémenter pour éviter une boucle infinie

    # Assigner le graphe à l'entrepôt
    entrepot.definir_graphe(graphe)
    logging.info(f"Fin de l'analyse du fichier. Produits lus: {len(entrepot.produits)}, Commandes lues: {len(entrepot.commandes)}")
    logging.info(f"Localisations lues: {len(graphe.locations)}, Arcs lus: {len(graphe.arcs)}")
    return entrepot
