"""
Classe `Room`.

Représente une pièce de la carte, ses sorties, son inventaire et les personnages présents.
"""

class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exits = {}
        self.inventory = {}
        self.characters = {}  # PNJ présents dans la salle

    def get_exit(self, direction):
        """Retourne la salle dans la direction donnée ou `None`."""
        return self.exits.get(direction, None)

    def get_exit_string(self):
        """Retourne une chaîne énumérant les sorties de la pièce."""
        exit_string = "Sorties: "
        for e in self.exits.keys():
            if self.exits.get(e) is not None:
                exit_string += e + ", "
        return exit_string.strip(", ")

    def get_long_description(self):
        """Description longue de la pièce, incluant les sorties."""
        return f"\nVous êtes dans {self.description}\n\n{self.get_exit_string()}\n"

    def get_inventory(self):
        """Retourne une chaîne décrivant les objets présents dans la pièce."""
        if len(self.inventory) == 0:
            return "\nIl n'y a rien ici.\n"
        result = "\nOn voit:\n"
        for item in self.inventory.values():
            result += f"    - {item}\n"
        result += "\n"
        return result
