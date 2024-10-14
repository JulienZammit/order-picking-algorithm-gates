# models/location.py

class Location:
    def __init__(self, id_location, x, y, name):
        self.id = id_location
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return f"Location(id={self.id}, x={self.x}, y={self.y}, name='{self.name}')"
