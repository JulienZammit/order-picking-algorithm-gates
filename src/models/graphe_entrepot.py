# models/graphe_entrepot.py

class GrapheEntrepot:
    """
    Classe représentant le graphe des déplacements dans l'entrepôt.
    """
    def __init__(self):
        """
        Initialise le graphe avec ses attributs.
        """
        self.arcs = {}          # Clé: (i, j), Valeur: distance directe
        self.distances = {}     # Clé: (i, j), Valeur: distance minimale
        self.depot_depart = None
        self.depot_arrivee = None
        self.produits = {}      # Référence aux produits pour accès rapide

    def ajouter_arc(self, depart, arrivee, distance):
        """
        Ajoute un arc au graphe.

        :param depart: Identifiant de la localisation de départ.
        :param arrivee: Identifiant de la localisation d'arrivée.
        :param distance: Distance entre les deux localisations.
        """
        self.arcs[(depart, arrivee)] = distance

    def ajouter_distance(self, depart, arrivee, distance):
        """
        Définit la plus courte distance entre deux localisations.

        :param depart: Identifiant de la localisation de départ.
        :param arrivee: Identifiant de la localisation d'arrivée.
        :param distance: Distance minimale entre les deux localisations.
        """
        self.distances[(depart, arrivee)] = distance

    def definir_depots(self, depot_depart, depot_arrivee):
        """
        Définit les dépôts de départ et d'arrivée.

        :param depot_depart: Identifiant du dépôt de départ.
        :param depot_arrivee: Identifiant du dépôt d'arrivée.
        """
        self.depot_depart = depot_depart
        self.depot_arrivee = depot_arrivee

    def __repr__(self):
        return f"GrapheEntrepot(arcs={len(self.arcs)}, distances={len(self.distances)})"
