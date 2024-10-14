# src/models/produit.py

class Produit:
    def __init__(self, id_produit, id_localisation, poids_unitaire, volume_unitaire, coordonnees= {}):
        self.id = id_produit
        self.localisation = id_localisation
        self.poids_unitaire = poids_unitaire
        self.volume_unitaire = volume_unitaire
        self.coordonnees = coordonnees  # Tuple (x, y)

    def __repr__(self):
        return f"Produit(id={self.id}, localisation={self.localisation}, poids={self.poids_unitaire}, volume={self.volume_unitaire}, coordonnees={self.coordonnees})"
