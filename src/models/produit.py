# models/produit.py

class Produit:
    """
    Classe représentant un produit dans l'entrepôt.
    """
    def __init__(self, id_produit, id_localisation, poids_unitaire, volume_unitaire):
        """
        Initialise un produit avec ses attributs.

        :param id_produit: Identifiant unique du produit.
        :param id_localisation: Identifiant de la localisation du produit dans l'entrepôt.
        :param poids_unitaire: Poids unitaire du produit.
        :param volume_unitaire: Volume unitaire du produit.
        """
        self.id = id_produit
        self.localisation = id_localisation
        self.poids_unitaire = poids_unitaire
        self.volume_unitaire = volume_unitaire

    def __repr__(self):
        return f"Produit(id={self.id}, localisation={self.localisation}, poids={self.poids_unitaire}, volume={self.volume_unitaire})"
