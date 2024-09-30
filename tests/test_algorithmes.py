# tests/test_algorithmes.py

import unittest
from models.colis import Colis
from models.produit import Produit

class TestAlgorithmes(unittest.TestCase):
    def test_ajouter_produit_colis(self):
        produit = Produit(1, 1, 2.0, 1.0)
        colis = Colis(1, 1)
        colis.ajouter_produit(produit, 3)
        self.assertEqual(colis.produits[1], 3)
        self.assertEqual(colis.poids_total, 6.0)
        self.assertEqual(colis.volume_total, 3.0)

if __name__ == '__main__':
    unittest.main()
