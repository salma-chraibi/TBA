# Définir la classe Player.
class Player():

    # Définir le constructeur.
    def __init__(self, name):
        self.name = name
        self.current_room = None
        self.history = []
        self.inventory = {}
    
    # Définir la méthode move.
    def move(self, direction):
        # Obtenir la pièce suivante à partir du dictionnaire exits de la pièce actuelle.
        next_room = self.current_room.exits.get(direction, None)

        # Si la pièce suivante est None, afficher un message d'erreur et retourner False.
        if next_room is None:
            print("\nAucune porte dans cette direction !\n")
            return False
        
        # Définir la pièce actuelle à la pièce suivante.
        self.current_room = next_room
        self.history.append(self.current_room)
        print(self.current_room.get_long_description())
        return True

    def get_inventory(self):
        """
        Retourne une chaîne représentant l'inventaire du joueur.
        
        Retourne:
            str: La chaîne représentant l'inventaire
        """
        if len(self.inventory) == 0:
            return "\nVotre inventaire est vide.\n"
        
        result = "\nVous disposez des items suivants:\n"
        for item in self.inventory.values():
            result += f"    - {item}\n"
        result += "\n"
        return result
