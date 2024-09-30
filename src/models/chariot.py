# models/chariot.py

class Chariot:
    """
    Classe représentant un chariot utilisé par un préparateur.
    """
    def __init__(self, id_chariot, capacite_max):
        """
        Initialise un chariot avec ses attributs.

        :param id_chariot: Identifiant unique du chariot.
        :param capacite_max: Capacité maximale en nombre de colis.
        """
        self.id = id_chariot
        self.capacite_max = capacite_max
        self.colis = []  # Liste des objets Colis

    def ajouter_colis(self, colis):
        """
        Ajoute un colis au chariot.

        :param colis: Objet Colis à ajouter.
        """
        if len(self.colis) < self.capacite_max:
            self.colis.append(colis)
        else:
            raise Exception("Capacité maximale du chariot atteinte.")

    def __repr__(self):
        return f"Chariot(id={self.id}, capacite_max={self.capacite_max}, colis={[colis.id for colis in self.colis]})"
