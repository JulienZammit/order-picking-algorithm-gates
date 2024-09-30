# main.py

import os
import logging

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
from algorithmes.algorithme_picking import (
    repartition_articles_colis,
    regroupement_colis_chariots,
    calcul_tournees,
)

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

        # Étape 5 : Validation de la solution
        solution_valide = valider_solution(entrepot, tournees)
        if solution_valide:
            logging.info(f"Solution pour {fichier_instance} est valide.")
        else:
            logging.error(f"Solution pour {fichier_instance} est invalide.")

if __name__ == "__main__":
    main()
