# tests/test_analyseur_instances.py

import sys
import os

# Ajouter le répertoire 'src' au chemin de recherche
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '../src'))
sys.path.insert(0, src_dir)

import unittest
from analyseur_instances import analyser_instance

class TestAnalyseurInstances(unittest.TestCase):
    def test_analyser_instance(self):
        # Construire le chemin complet vers le fichier d'instance
        chemin_fichier = os.path.abspath(os.path.join(current_dir, '../data/instances/instance_0116_131933_Z2.txt'))
        entrepot = analyser_instance(chemin_fichier)
        
        # Afficher l'entrepôt
        print(entrepot)
        
        # Vérifier que l'entrepôt n'est pas None
        self.assertIsNotNone(entrepot)
        
        # Vérifier le nombre de produits
        self.assertEqual(len(entrepot.produits), 401, "Le nombre de produits doit être 401.")
        
        # Vérifier le nombre de commandes
        self.assertEqual(len(entrepot.commandes), 6, "Le nombre de commandes doit être 6.")
        
        # Vérifier les capacités du colis
        self.assertEqual(entrepot.capacite_colis, (12000.0, 92160.0), "Les capacités du colis ne sont pas correctes.")
        
        # Vérifier la capacité du chariot
        self.assertEqual(entrepot.capacite_chariot, 6, "La capacité du chariot doit être 6.")
        
        # Vérifier quelques produits spécifiques
        produit1 = entrepot.produits.get(1)
        self.assertIsNotNone(produit1, "Le produit 1 doit exister.")
        self.assertEqual(produit1.localisation, 193, "La localisation du produit 1 doit être 193.")
        self.assertEqual(produit1.poids_unitaire, 2.0, "Le poids unitaire du produit 1 doit être 2.0.")
        self.assertEqual(produit1.volume_unitaire, 165.0, "Le volume unitaire du produit 1 doit être 165.0.")
        
        # Vérifier une commande spécifique
        commande1 = entrepot.commandes.get(1)
        self.assertIsNotNone(commande1, "La commande 1 doit exister.")
        self.assertEqual(commande1.mc, 6, "Le nombre maximal de colis pour la commande 1 doit être 6.")
        self.assertEqual(len(commande1.lignes_commande), 115, "La commande 1 doit contenir 115 lignes de commande.")
        
        # Vérifier que le graphe est correctement défini
        self.assertIsNotNone(entrepot.graphe, "Le graphe doit être défini.")
        
        print("Test réussi : les données de l'instance ont été correctement analysées.")

if __name__ == '__main__':
    unittest.main()
