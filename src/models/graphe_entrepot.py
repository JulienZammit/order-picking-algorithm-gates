# models/graphe_entrepot.py

from models.location import Location
from models.arc import Arc

class GrapheEntrepot:
    """
    Classe représentant le graphe des déplacements dans l'entrepôt.
    """
    def __init__(self):
        """
        Initialise le graphe avec ses attributs.
        """
        self.locations = {}      # Clé: id de la localisation, Valeur: objet Location
        self.arcs = []           # Liste des arcs (objets Arc)
        self.distances = {}      # Clé: (i, j), Valeur: distance minimale
        self.depot_depart = None
        self.depot_arrivee = None
        self.produits = {}       # Référence aux produits pour accès rapide

    def ajouter_arc(self, arc: Arc):
        """
        Ajoute un arc au graphe.

        :param arc: Objet Arc à ajouter.
        """
        self.arcs.append(arc)
        self.distances[(arc.start, arc.end)] = arc.distance

    def ajouter_location(self, location: Location):
        """
        Ajoute une localisation au graphe.

        :param location: Objet Location à ajouter.
        """
        self.locations[location.id] = location

    def obtenir_location(self, id_location):
        """
        Récupère une localisation par son identifiant.

        :param id_location: Identifiant de la localisation.
        :return: Objet Location ou None si non trouvé.
        """
        return self.locations.get(id_location, None)

    def obtenir_arc(self, depart, arrivee):
        """
        Récupère un arc entre deux localisations, s'il existe.

        :param depart: Identifiant de la localisation de départ.
        :param arrivee: Identifiant de la localisation d'arrivée.
        :return: Objet Arc ou None si non trouvé.
        """
        for arc in self.arcs:
            if arc.start == depart and arc.end == arrivee:
                return arc
        return None

    def definir_depots(self, depot_depart, depot_arrivee):
        """
        Définit les dépôts de départ et d'arrivée.

        :param depot_depart: Identifiant du dépôt de départ.
        :param depot_arrivee: Identifiant du dépôt d'arrivée.
        """
        self.depot_depart = depot_depart
        self.depot_arrivee = depot_arrivee

    def calculer_tous_plus_courts_chemins(self):
        """
        Calcule les distances minimales entre toutes les paires de localisations
        en utilisant l'algorithme de Floyd-Warshall.
        """
        # Initialisation de la matrice des distances
        nodes = list(self.locations.keys())
        n = len(nodes)
        self.all_pairs_distances = {i: {j: float('inf') for j in nodes} for i in nodes}

        # Distance de chaque nœud à lui-même est 0
        for node in nodes:
            self.all_pairs_distances[node][node] = 0

        # Initialisation avec les distances directes
        for arc in self.arcs:
            self.all_pairs_distances[arc.start][arc.end] = arc.distance

        # Algorithme de Floyd-Warshall
        for k in nodes:
            for i in nodes:
                for j in nodes:
                    if self.all_pairs_distances[i][j] > self.all_pairs_distances[i][k] + self.all_pairs_distances[k][j]:
                        self.all_pairs_distances[i][j] = self.all_pairs_distances[i][k] + self.all_pairs_distances[k][j]

    def shortest_path_length(self, start, end):
        """
        Retourne la distance minimale entre deux localisations.
        Doit être appelé après calculer_tous_plus_courts_chemins.
        """
        return self.all_pairs_distances.get(start, {}).get(end, float('inf'))

    def __repr__(self):
        return f"GrapheEntrepot(nb_locations={len(self.locations)}, nb_arcs={len(self.arcs)}, distances={len(self.distances)})"
