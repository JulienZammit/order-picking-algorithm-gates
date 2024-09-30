# models/commande.py

class Commande:
    """
    Classe représentant une commande client.
    """
    def __init__(self, id_commande, mc):
        """
        Initialise une commande avec ses attributs.

        :param id_commande: Identifiant unique de la commande.
        :param mc: Nombre maximal de colis pour la commande.
        """
        self.id = id_commande
        self.mc = mc
        self.lignes_commande = {}  # Clé: id_produit, Valeur: quantité

    def ajouter_produit(self, id_produit, quantite):
        """
        Ajoute un produit à la commande.

        :param id_produit: Identifiant du produit.
        :param quantite: Quantité commandée du produit.
        """
        self.lignes_commande[id_produit] = quantite

    def __repr__(self):
        return f"Commande(id={self.id}, mc={self.mc}, lignes_commande={self.lignes_commande})"
