# main.py

import os
import logging
import pandas as pd
# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler("debug.log", mode='w'),
        logging.StreamHandler()
    ]
)

from analyseur_instances import analyser_instance
from generateur_solutions import generer_fichier_solution
from utils.validation import valider_solution
from algorithmes.algorithme_picking_V3 import (
    repartition_articles_colis,
    regroupement_colis_chariots,
    calcul_tournees,
)
def generer_excel_taux_remplissage(nom_instance, colis_list):
    """
    Génère un fichier Excel avec les informations sur les colis et leur taux de remplissage.
    
    :param nom_instance: Nom de l'instance.
    :param colis_list: Liste des colis à analyser.
    """
    data = []

    for colis in colis_list:
        taux_remplissage = colis.taux_remplissage() * 100  # En pourcentage
        data.append({
            'instance': nom_instance,
            'commande': colis.id_commande,
            'colis': colis.id,
            'taux_remplissage (%)': taux_remplissage
        })

    # Créer un DataFrame et sauvegarder en Excel
    df = pd.DataFrame(data)
    chemin_fichier_excel = f"data/excel/{nom_instance}_remplissage.xlsx"
    os.makedirs(os.path.dirname(chemin_fichier_excel), exist_ok=True)
    df.to_excel(chemin_fichier_excel, index=False)
    logging.info(f"Fichier Excel généré: {chemin_fichier_excel}")
def main():
    dossier_instances = "data/instances/"
    fichiers_instances = [f for f in os.listdir(dossier_instances) if f.endswith('.txt')]

    for fichier_instance in fichiers_instances:
        chemin_instance = os.path.join(dossier_instances, fichier_instance)
        logging.info(f"Traitement de l'instance : {fichier_instance}")
        entrepot = analyser_instance(chemin_instance)

        # Étape 1 : Répartition des articles dans les colis
        colis_list = repartition_articles_colis(entrepot)

        # Étape 2 : Regroupement des colis sur les chariots
        chariots = regroupement_colis_chariots(entrepot, colis_list)

        # Vérifier si des chariots ont été créés
        if not chariots:
            logging.warning(f"Aucun chariot n'a pu être créé pour l'instance {fichier_instance}.")
            continue

        # Étape 3 : Calcul des tournées
        tournees = calcul_tournees(entrepot, chariots)

        # Étape 4 : Génération du fichier de solution
        nom_instance = fichier_instance.replace('.txt', '')
        generer_fichier_solution(nom_instance, tournees)
        generer_excel_taux_remplissage(nom_instance, colis_list)

        # Étape 5 : Validation de la solution
        solution_valide = valider_solution(entrepot, tournees)
        if solution_valide:
            logging.info(f"Solution pour {fichier_instance} est valide.")
        else:
            logging.error(f"Solution pour {fichier_instance} est invalide.")

if __name__ == "__main__":
    main()
