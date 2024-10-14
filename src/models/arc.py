# models/arc.py

class Arc:
    def __init__(self, start, end, distance):
        self.start = start  # ID de la localisation de départ
        self.end = end      # ID de la localisation d'arrivée
        self.distance = distance

    def __repr__(self):
        return f"Arc(start={self.start}, end={self.end}, distance={self.distance})"
