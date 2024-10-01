# tests/test_generateur_solutions.py

import sys
import os

# Ajouter le répertoire 'src' au chemin de recherche
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_dir)

import unittest
from models.chariot import Chariot
from models.colis import Colis
from models.tournee import Tournee
from generateur_solutions import generer_fichier_solution

class TestGenerateurSolutions(unittest.TestCase):
    def test_generer_fichier_solution(self):
        # Création de données factices
        # Tournée 1 avec 2 colis
        chariot1 = Chariot(1, 2)
        colis1 = Colis(1, 1, 12000.0, 92160.0)  # Colis ID 1, Commande ID 1
        colis1.produits = {1: 2, 2: 1}  # Produit ID 1: qty 2, Produit ID 2: qty 1
        colis2 = Colis(2, 2, 12000.0, 92160.0)  # Colis ID 2, Commande ID 2
        colis2.produits = {3: 1, 4: 3}
        chariot1.ajouter_colis(colis1)
        chariot1.ajouter_colis(colis2)
        tournee1 = Tournee(1, chariot1)
        
        # Tournée 2 avec 1 colis
        chariot2 = Chariot(2, 2)
        colis3 = Colis(3, 1, 12000.0, 92160.0)
        colis3.produits = {5: 2}
        chariot2.ajouter_colis(colis3)
        tournee2 = Tournee(2, chariot2)
        
        tournees = [tournee1, tournee2]

        nom_instance = 'test_instance'
        generer_fichier_solution(nom_instance, tournees)
        chemin_fichier = os.path.abspath(os.path.join(current_dir, f"../data/solutions/{nom_instance}_sol.txt"))
        self.assertTrue(os.path.exists(chemin_fichier), "Le fichier de solution n'a pas été créé.")
        
        # Lire le contenu du fichier généré
        with open(chemin_fichier, 'r') as fichier:
            contenu = fichier.read()
        
        # Préparer le contenu attendu
        contenu_attendu = """//NbTournees
2
//IdTournes NbColis
1 2
//IdColis IdCommandeInColis NbProducts IdProd1 QtyProd1 IdProd2 QtyProd2 ...
1 1 2 1 2 2 1
2 2 2 3 1 4 3
//IdTournes NbColis
2 1
//IdColis IdCommandeInColis NbProducts IdProd1 QtyProd1 IdProd2 QtyProd2 ...
3 1 1 5 2
"""
        # Comparer le contenu généré avec le contenu attendu
        self.assertEqual(contenu.strip(), contenu_attendu.strip(), "Le contenu du fichier généré ne correspond pas au contenu attendu.")
        
        # Nettoyage
        os.remove(chemin_fichier)

if __name__ == '__main__':
    unittest.main()
