# models/tournee.py

class Tournee:
    """
    Classe représentant une tournée de picking effectuée par un préparateur.
    """
    def __init__(self, id_tournee, chariot):
        """
        Initialise une tournée avec ses attributs.

        :param id_tournee: Identifiant unique de la tournée.
        :param chariot: Objet Chariot associé à la tournée.
        """
        self.id = id_tournee
        self.chariot = chariot
        self.sequence_localisations = []  # Liste ordonnée des localisations à visiter
        self.distance_totale = 0

    def calculer_sequence(self, graphe):
        """
        Calcule la séquence de localisations à visiter en fonction des produits à ramasser.

        :param graphe: Objet GrapheEntrepot pour calculer les distances.
        """
        # Implémentation simplifiée pour l'exemple
        localisations = set()
        for colis in self.chariot.colis:
            for id_produit in colis.produits:
                localisations.add(graphe.produits[id_produit].localisation)

        self.sequence_localisations = sorted(localisations)
        self.distance_totale = self.calculer_distance_totale(graphe)

    def calculer_distance_totale(self, graphe):
        """
        Calcule la distance totale de la tournée.

        :param graphe: Objet GrapheEntrepot.
        :return: Distance totale parcourue.
        """
        distance = 0
        # Implémentation simplifiée pour l'exemple
        if self.sequence_localisations:
            current = graphe.depot_depart
            for loc in self.sequence_localisations:
                distance += graphe.distances.get((current, loc), float('inf'))
                current = loc
            distance += graphe.distances.get((current, graphe.depot_arrivee), float('inf'))
        return distance

    def __repr__(self):
        return f"Tournee(id={self.id}, distance_totale={self.distance_totale}, sequence={self.sequence_localisations})"
