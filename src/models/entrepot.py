# models/entrepot.py

class Entrepot:
    """
    Classe représentant la zone de picking de l'entrepôt.
    """
    def __init__(self):
        """
        Initialise l'entrepôt avec ses attributs.
        """
        self.localisations = {}  # Clé: id_localisation, Valeur: (x, y, type)
        self.produits = {}       # Clé: id_produit, Valeur: objet Produit
        self.commandes = {}      # Clé: id_commande, Valeur: objet Commande
        self.graphe = None       # Objet GrapheEntrepot
        self.depot_depart = None
        self.depot_arrivee = None
        self.capacite_colis = (0, 0)  # (poids_max, volume_max)
        self.capacite_chariot = 0

    def ajouter_produit(self, produit):
        """
        Ajoute un produit à l'entrepôt.

        :param produit: Objet Produit.
        """
        self.produits[produit.id] = produit

    def ajouter_commande(self, commande):
        """
        Ajoute une commande à l'entrepôt.

        :param commande: Objet Commande.
        """
        self.commandes[commande.id] = commande

    def definir_graphe(self, graphe):
        """
        Définit le graphe de l'entrepôt.

        :param graphe: Objet GrapheEntrepot.
        """
        self.graphe = graphe
        self.depot_depart = graphe.depot_depart
        self.depot_arrivee = graphe.depot_arrivee

    def __repr__(self):
        return f"Entrepot(produits={len(self.produits)}, commandes={len(self.commandes)})"
