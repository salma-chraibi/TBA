"""Module des actions.

Ce module contient les fonctions appelées lors de l'exécution d'une commande.
Chaque fonction prend 3 paramètres :
- game : l'objet jeu
- list_of_words : la liste des mots de la commande
- number_of_parameters : le nombre de paramètres attendus

Les fonctions retournent True si la commande a été exécutée correctement, False sinon.
Elles affichent un message d'erreur si le nombre de paramètres est incorrect.

Les messages d'erreur sont stockés dans `MSG0` et `MSG1` formatés avec le mot de la commande.
`MSG0` est utilisé pour les commandes sans paramètre.
"""
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# Le message utilisé lorsque la commande prend 1 paramètre.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Déplace le joueur dans la direction indiquée en paramètre.
        Le paramètre attendu est une direction cardinale (N, E, S, O, U, D).

        Paramètres:
            game (Game): l'objet jeu.
            list_of_words (list): la liste des mots de la commande.
            number_of_parameters (int): le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a réussi, False sinon.
        """
        
        
        player = game.player
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        # Get the direction from the list of words.
        direction = list_of_words[1]
        # Move the player in the direction specified by the parameter.
        player.move(direction)
        return True



    def quit(game, list_of_words, number_of_parameters):
        """
        Quitte le jeu.

        Paramètres:
            game (Game): l'objet jeu.
            list_of_words (list): la liste des mots de la commande.
            number_of_parameters (int): le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a réussi, False sinon.
        """
        l = len(list_of_words)
        # If the number of parameters is incorrect, print an error message and return False.
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Set the finished attribute of the game object to True.
        player = game.player
        msg = f"\nMerci {player.name} d'avoir joué. Au revoir.\n"
        print(msg)
        game.finished = True
        return True

    def help(game, list_of_words, number_of_parameters):
        """
        Affiche la liste des commandes disponibles.

        Paramètres:
            game (Game): l'objet jeu.
            list_of_words (list): la liste des mots de la commande.
            number_of_parameters (int): le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a réussi, False sinon.
        """

        # If the number of parameters is incorrect, print an error message and return False.
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Print the list of available commands.
        print("\nVoici les commandes disponibles:")
        for command in game.commands.values():
            print("\t- " + str(command))
        print()
        return True

    def back(game, list_of_words, number_of_parameters):
        """
        Revenir à la pièce précédente.

        Paramètres:
            game (Game): l'objet jeu.
            list_of_words (list): la liste des mots de la commande.
            number_of_parameters (int): le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a réussi, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        if len(player.history) > 1:
            player.history.pop()
            player.current_room = player.history[-1]
            print(player.current_room.get_long_description())
            print(Actions.get_history(player))
            return True
        else:
            print("\nVous ne pouvez pas revenir plus loin.\n")
            return False

    def history(game, list_of_words, number_of_parameters):
        """
        Affiche l'historique des pièces visitées.

        Paramètres:
            game (Game): l'objet jeu.
            list_of_words (list): la liste des mots de la commande.
            number_of_parameters (int): le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a réussi, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(Actions.get_history(player))
        return True

    def get_history(player):
        """
        Retourne une chaîne représentant l'historique des pièces visitées.

        Paramètres:
            player (Player): L'objet joueur.

        Retourne:
            str: La chaîne formatée de l'historique.
        """
        if len(player.history) <= 1:
            return "\nVous n'avez visité aucune pièce précédemment.\n"
        result = "\nVous avez déja visité les pièces suivantes:\n"
        for room in player.history[:-1]:
            result += f"    - {room.description}\n"
        result += "\n"
        return result

    def look(game, list_of_words, number_of_parameters):
        """
        Affiche la description de la pièce, les items et les PNJ.

        Paramètres:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots de la commande.
            number_of_parameters (int): Le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a été exécutée avec succès, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        room = player.current_room
        
        # Afficher les items
        if len(room.inventory) > 0:
            print("\nOn voit:")
            for item in room.inventory.values():
                print(f"    - {item}")
        else:
            print("\nIl n'y a rien ici.")
        
        # Afficher les personnages
        if len(room.characters) > 0:
            print("\nPersonnages présents:")
            for character in room.characters.values():
                print(f"    - {character}")
        
        print()
        return True

    def take(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de prendre un item dans la pièce.

        Paramètres:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots de la commande.
            number_of_parameters (int): Le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a été exécutée avec succès, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        item_name = list_of_words[1]
        
        # Vérifier si l'item existe dans la pièce
        if item_name not in player.current_room.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans la pièce.\n")
            return False
        
        # Prendre l'item
        item = player.current_room.inventory.pop(item_name)
        player.inventory[item_name] = item
        print(f"\nVous avez pris l'objet '{item_name}'.\n")
        return True

    def drop(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de déposer un item dans la pièce.

        Paramètres:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots de la commande.
            number_of_parameters (int): Le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a été exécutée avec succès, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        item_name = list_of_words[1]
        
        # Vérifier si l'item existe dans l'inventaire
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans l'inventaire'.\n")
            return False
        
        # Déposer l'item
        item = player.inventory.pop(item_name)
        player.current_room.inventory[item_name] = item
        print(f"\nVous avez déposé l'objet '{item_name}'.\n")
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        Affiche l'inventaire du joueur.

        Paramètres:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots de la commande.
            number_of_parameters (int): Le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a été exécutée avec succès, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        print(player.get_inventory())
        return True

    def wait(game, list_of_words, number_of_parameters):
        """
        Faire avancer les PNJ d'un pas (commande manuelle 'wait').

        Paramètres:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots de la commande.
            number_of_parameters (int): Le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a réussi, False sinon.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        try:
            game.update_characters()
            return True
        except Exception:
            print("\nImpossible d'avancer les PNJ pour le moment.\n")
            return False

    def talk(game, list_of_words, number_of_parameters):
        """
        Permet au joueur de parler à un personnage dans la pièce.

        Paramètres:
            game (Game): L'objet jeu.
            list_of_words (list): La liste des mots de la commande.
            number_of_parameters (int): Le nombre de paramètres attendus.

        Retourne:
            bool: True si la commande a été exécutée avec succès, False sinon.
        """
        l = len(list_of_words)
        # Autoriser les noms composés (plusieurs mots) pour le PNJ :
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room
        target_name = " ".join(list_of_words[1:])
        
        # Vérifier si le personnage existe dans la pièce
        character = room.characters.get(target_name, None)
        if character is None:
            print(f"\nIl n'y a pas de personnage nommé '{target_name}' ici.\n")
            return False
        
        # Afficher le message du personnage
        print(character.get_msg())
        return True