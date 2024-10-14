# models/commande.py

class Commande:
    def __init__(self, id_commande, mc):
        self.id = id_commande
        self.mc = mc  # Nombre de colis pour cette commande
        self.lignes_commande = {}  # Clé: id_produit, Valeur: quantite
        self.coordonnees_produits = {}  # Clé: id_produit, Valeur: coordonnees (x, y)

    def ajouter_produit(self, id_produit, quantite, coordonnees=None):
        if id_produit in self.lignes_commande:
            self.lignes_commande[id_produit] += quantite
        else:
            self.lignes_commande[id_produit] = quantite
        if coordonnees:
            self.coordonnees_produits[id_produit] = coordonnees
