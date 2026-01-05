# Description: Classe Character pour les PNJ

import random

import game

class Character:
    """
    Classe pour représenter un personnage non-joueur (PNJ).
    
    Attributs:
        name (str): Le nom du personnage
        description (str): La description du personnage
        current_room (Room): La pièce actuelle du personnage
        msgs (list): La liste des messages que le personnage peut dire
    """
    
    def __init__(self, name, description, current_room, msgs):
        """
        Initialise un Character.
        
            Paramètres:
                name (str): Le nom du personnage
                description (str): La description du personnage
                current_room (Room): La pièce actuelle du personnage
                msgs (list): La liste des messages que le personnage peut dire
        """
        self.name = name
        self.description = description
        self.current_room = current_room
        self.msgs = msgs[:]  # copie de la liste des messages
        self._msg_index = 0  # pour suivre quel message afficher
        # Liste optionnelle des salles (objets Room) où ce PNJ est autorisé à aller.
        # None signifie aucune restriction (peut aller partout).
        self.allowed_rooms = None
    
    def __str__(self):
        """
        Retourne une représentation textuelle du personnage.
        
            Retourne:
            str: Une chaîne au format "nom : description"
        """
        return f"{self.name} : {self.description}"
    
    def get_msg(self):
        """
        Retourne cycliquement les messages du PNJ.

            Retourne:
            str: Le message du PNJ formaté
        """
        if not self.msgs:
            return f"{self.name} ne dit rien..."
        msg = self.msgs[self._msg_index]
        self._msg_index = (self._msg_index + 1) % len(self.msgs)
        return f"\n{self.name} : {msg}\n"
    
    def move(self):
        """
        Le PNJ a une chance sur deux de se déplacer dans une salle adjacente.

            Retourne:
            bool: True si le PNJ s'est déplacé, False sinon
        """
        # Ne permettre le déplacement que pour le PNJ 'Durand'
        if self.name != "Durand":
            return False

        # Si une liste d'autorisations est définie, ne tenter le tirage
        # aléatoire (chance 1/2) que si le PNJ se trouve dans une salle autorisée.
        if self.allowed_rooms is not None and self.current_room not in self.allowed_rooms:
            return False

        if random.choice([True, False]):
            exits = [room for room in self.current_room.exits.values() if room is not None]
            # Si une liste d'autorisations est définie, ne retenir que les sorties autorisées.
            # Si aucune sortie autorisée n'est présente, le PNJ ne se déplace pas.
            if self.allowed_rooms is not None:
                allowed_set = set(self.allowed_rooms)
                allowed_exits = [r for r in exits if r in allowed_set]
                if allowed_exits:
                    exits = allowed_exits
                else:
                    return False
            if exits:
                new_room = random.choice(exits)
                if game.DEBUG:
                    print(f"DEBUG: {self.name} se déplace vers {new_room.name}")
                self.current_room.characters.pop(self.name, None)
                self.current_room = new_room
                self.current_room.characters[self.name] = self
                return True
        return False
