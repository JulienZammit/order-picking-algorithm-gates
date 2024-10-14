# models/colis.py

from models.produit import Produit
import logging
logger = logging.getLogger(__name__)

class Colis:
    """
    Classe représentant un colis contenant des articles pour une commande spécifique.
    """
    def __init__(self, id_colis, id_commande, poids_max, volume_max):
        """
        Initialise un colis avec ses attributs.

        :param id_colis: Identifiant unique du colis.
        :param id_commande: Identifiant de la commande associée.
        """
        self.id = id_colis
        self.id_commande = id_commande
        self.produits = {}
        self.poids_total = 0.0
        self.volume_total = 0.0
        self.poids_max = poids_max
        self.volume_max = volume_max

    def ajouter_produit(self, produit, quantite):
        """
        Ajoute un produit dans le colis.

        :param produit: Objet Produit.
        :param quantite: Quantité à ajouter.
        """
        if produit.id in self.produits:
            self.produits[produit.id] += quantite
        else:
            self.produits[produit.id] = quantite

        self.poids_total += produit.poids_unitaire * quantite
        self.volume_total += produit.volume_unitaire * quantite
    def centre_gravite(self, entrepot):
        positions = [entrepot.produits[id_prod].localisation for id_prod in self.produits]
        return sum(positions) / len(positions) if positions else 0    
    def peut_ajouter_produit(self, produit, quantite):
        """
        Vérifie quelle quantité du produit peut être ajoutée dans le colis.

        :param produit: Objet Produit.
        :param quantite: Quantité demandée à ajouter.
        :return: Quantité effectivement ajoutée.
        """
        poids_unitaire = produit.poids_unitaire
        volume_unitaire = produit.volume_unitaire

        # Vérifier que le poids et le volume unitaires sont positifs
        if poids_unitaire <= 0 or volume_unitaire <= 0:
            logger.error(f"Produit {produit.id} a un poids ou volume unitaire nul ou négatif.")
            return 0

        # Vérifier si le produit peut entrer dans le colis en un seul exemplaire
        if poids_unitaire > self.poids_max or volume_unitaire > self.volume_max:
            return 0

        # Calculer le poids et le volume disponibles dans le colis
        poids_disponible = self.poids_max - self.poids_total
        volume_disponible = self.volume_max - self.volume_total

        # Calculer la quantité maximale pouvant être ajoutée en fonction du poids
        quantite_max_poids = poids_disponible / poids_unitaire
        # Calculer la quantité maximale pouvant être ajoutée en fonction du volume
        quantite_max_volume = volume_disponible / volume_unitaire

        # La quantité maximale possible est la plus petite des trois valeurs :
        # quantite_max_poids, quantite_max_volume, quantite demandée
        quantite_max_possible = min(quantite_max_poids, quantite_max_volume, quantite)

        # Prendre la partie entière inférieure de la quantité maximale possible
        quantite_max_possible = int(quantite_max_possible)

        # Retourner la quantité maximale possible, en s'assurant qu'elle est positive
        return max(0, quantite_max_possible)


    def taux_remplissage(self):
        """
        Calcule le taux de remplissage du colis en fonction du volume.
        
        :return: Un pourcentage (valeur entre 0 et 1) représentant le taux de remplissage du colis.
        """
        if self.volume_max > 0:
            return self.volume_total / self.volume_max
        return 0

    def __repr__(self):
        return f"Colis(id={self.id}, id_commande={self.id_commande}, poids_total={self.poids_total}, volume_total={self.volume_total}, produits={self.produits})"