import os
import subprocess
import pandas as pd
import re

def main():
    # Nettoyer les fichiers indésirables
    clean_zone_identifier_files()

    # Récupérer la liste des instances
    instance_files = get_instance_files()

    # Initialiser une liste pour stocker les résultats
    results = []

    # Parcourir chaque instance
    for instance_file in instance_files:
        # Extraire le nom de l'instance sans l'extension '.txt'
        instance_name = os.path.splitext(instance_file)[0]
        print(f"Traitement de l'instance : {instance_name}")

        # Exécuter le checker
        output = run_checker(instance_name)

        # Vérifier si le checker a échoué
        if 'Checking FAILED' in output:
            print(f"Checker a échoué pour l'instance {instance_name}.")
            continue

        # Analyser la sortie pour extraire les données
        number_of_tours, number_of_parcels, total_distance = parse_output(output)

        # Vérifier que les données ont été correctement extraites
        if number_of_tours is not None and number_of_parcels is not None and total_distance is not None:
            # Ajouter les données aux résultats
            results.append({
                'Instance': instance_name,
                'Number of Tours': number_of_tours,
                'Number of Parcels': number_of_parcels,
                'Total Distance (m)': total_distance
            })
        else:
            print(f"Impossible d'extraire les données pour l'instance {instance_name}.")

    # Créer un DataFrame pandas à partir des résultats
    df = pd.DataFrame(results)

    # Enregistrer le DataFrame dans un fichier Excel
    df.to_excel('results.xlsx', index=False)
    print("Le fichier results.xlsx a été généré avec succès.")

def clean_zone_identifier_files():
    """
    Supprime les fichiers dont le nom se termine par ':Zone.Identifier'.
    """
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(':Zone.Identifier'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Fichier supprimé : {file_path}")
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier {file_path}: {e}")

def get_instance_files():
    """
    Récupère la liste des fichiers d'instance (fichiers .txt sans '_sol' dans le nom).
    """
    files = [f for f in os.listdir('.') if f.endswith('.txt') and '_sol' not in f]
    return files

def run_checker(instance_name):
    """
    Exécute le checker Java pour une instance donnée et renvoie la sortie.
    """
    cmd = ['java', '-jar', 'CheckerBatchingPicking.jar', instance_name]
    try:
        # Exécuter la commande et capturer la sortie
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        # En cas d'erreur, retourner quand même la sortie
        return e.output
    except FileNotFoundError:
        print("Erreur : Java n'est pas installé ou n'est pas dans le PATH.")
        return ""

def parse_output(output):
    """
    Analyse la sortie du checker pour extraire le nombre de tournées, le nombre de colis et la distance totale.
    """
    number_of_tours = None
    number_of_parcels = None
    total_distance = None

    # Diviser la sortie en lignes
    lines = output.splitlines()
    for line in lines:
        line = line.strip()
        if '--> Nombre de tournees :' in line:
            # Extraire le nombre de tournées
            match = re.search(r'--> Nombre de tournees :\s*(\d+)', line)
            if match:
                number_of_tours = int(match.group(1))
        elif '--> Nombre de colis :' in line:
            # Extraire le nombre de colis
            match = re.search(r'--> Nombre de colis :\s*(\d+)', line)
            if match:
                number_of_parcels = int(match.group(1))
        elif '--> Distance totale :' in line:
            # Extraire la distance totale en gérant le format français
            match = re.search(r'--> Distance totale :\s*([\d\s,]+) m\.', line)
            if match:
                distance_str = match.group(1)
                # Supprimer les espaces
                distance_str = distance_str.replace(' ', '')
                # Remplacer la virgule par un point
                distance_str = distance_str.replace(',', '.')
                try:
                    total_distance = float(distance_str)
                except ValueError:
                    total_distance = None

    return number_of_tours, number_of_parcels, total_distance

if __name__ == '__main__':
    main()
