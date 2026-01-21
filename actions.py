"""Action module.

This module contains the functions called when executing a command.
Each function takes 3 parameters:
- game: the game object
- list_of_words: the list of words from the command
- number_of_parameters: the number of expected parameters

The functions return True if the command was executed correctly, False otherwise.
They display an error message if the number of parameters is incorrect.

Error messages are stored in `MSG0` and `MSG1` formatted with the command word.
`MSG0` is used for commands without parameters.
"""
MSG0 = "\nLa commande '{command_word}' ne prend pas de paramètre.\n"
# The message used when the command takes 1 parameter.
MSG1 = "\nLa commande '{command_word}' prend 1 seul paramètre.\n"

class Actions:

    def go(game, list_of_words, number_of_parameters):
        """
        Move the player in the direction specified as a parameter.
        The expected parameter is a cardinal direction (N, E, S, O, U, D).

        Parameters:
            game (Game): the game object.
            list_of_words (list): the list of words from the command.
            number_of_parameters (int): the number of expected parameters.

        Returns:
            bool: True if the command succeeded, False otherwise.
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
        # Store current room before moving
        old_room = player.current_room
        # Move the player in the direction specified by the parameter.
        player.move(direction)
        # Check if player actually moved
        new_room = player.current_room
        if old_room != new_room:
            # Track crime scene rooms for Quest 1
            if new_room.name in ["Grenier", "Maison du crime", "Cave", "Jardin"]:
                game.visited_crime_scene_rooms.add(new_room.name)
                # Check if Quest 1 should be completed
                game.check_quest1_completion()
            
            # Count displacement if not in excluded rooms
            excluded_rooms = {"Grenier", "Jardin", "Cave", "Labo du commissariat"}
            if new_room.name not in excluded_rooms and old_room.name not in excluded_rooms:
                game.displacement_count += 1
                
                # Display daily reminder every 10 displacements
                if game.displacement_count % 10 == 0:
                    day_number = game.displacement_count // 10
                    remaining_moves = 40 - game.displacement_count
                    remaining_days = 4 - day_number
                    
                    print("\n" + "="*60)
                    print(f"FIN DU JOUR {day_number}")
                    print("="*60)
                    print(f"Déplacements effectués: {game.displacement_count}/40")
                    print(f"Déplacements restants: {remaining_moves}")
                    print(f"Jours restants: {remaining_days}")
                    print("="*60 + "\n")
                    
                    if remaining_days == 0:
                        print("ATTENTION: Vous manquez de temps!\n")
                else:
                    remaining_moves = 40 - game.displacement_count
                    remaining_days = (remaining_moves / 40) * 4
                    print(f"Déplacements: {game.displacement_count}/40 | Temps restant: ≈ {remaining_days:.1f} jours")
                    if remaining_moves <= 5:
                        print("ATTENTION: Vous manquez de temps!")
        return True



    def quit(game, list_of_words, number_of_parameters):
        """
        Quit the game.

        Parameters:
            game (Game): the game object.
            list_of_words (list): the list of words from the command.
            number_of_parameters (int): the number of expected parameters.

        Returns:
            bool: True if the command succeeded, False otherwise.
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
        Display the list of available commands.

        Parameters:
            game (Game): the game object.
            list_of_words (list): the list of words from the command.
            number_of_parameters (int): the number of expected parameters.

        Returns:
            bool: True if the command succeeded, False otherwise.
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
        Return to the previous room.

        Parameters:
            game (Game): the game object.
            list_of_words (list): the list of words from the command.
            number_of_parameters (int): the number of expected parameters.

        Returns:
            bool: True if the command succeeded, False otherwise.
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
        Display the history of visited rooms.

        Parameters:
            game (Game): the game object.
            list_of_words (list): the list of words from the command.
            number_of_parameters (int): the number of expected parameters.

        Returns:
            bool: True if the command succeeded, False otherwise.
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
        Return a string representing the history of visited rooms.

        Parameters:
            player (Player): The player object.

        Returns:
            str: The formatted history string.
        """
        if len(player.history) <= 1:
            return "\nVous n'avez visité aucune pièce précédemment.\n"
        result = "\nVous avez déjà visité les pièces suivantes:\n"
        for room in player.history[:-1]:
            result += f"    - {room.description}\n"
        result += "\n"
        return result

    def look(game, list_of_words, number_of_parameters):
        """
        Display the room description, items, and NPCs.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        player = game.player
        room = player.current_room
        
        # Display items
        if len(room.inventory) > 0:
            print("\nOn voit:")
            for item in room.inventory.values():
                print(f"    - {item}")
        else:
            print("\nIl n'y a rien ici.")
        
        # Display characters
        if len(room.characters) > 0:
            print("\nPersonnages présents:")
            for character in room.characters.values():
                print(f"    - {character}")
        
        print()
        return True

    def take(game, list_of_words, number_of_parameters):
        """
        Allow the player to take an item from the room.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        item_name = list_of_words[1]
        
        # Check if the item exists in the room
        if item_name not in player.current_room.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans la pièce.\n")
            return False
        
        # Take the item
        item = player.current_room.inventory.pop(item_name)
        player.inventory[item_name] = item
        print(f"\nVous avez pris l'objet '{item_name}'.\n")
        
        # Track items for Quest 1
        if item_name in ["photos", "knife", "chest", "weapon"]:
            game.collected_items.add(item_name)
            # Check if Quest 1 should be completed
            game.check_quest1_completion()
        
        return True

    def drop(game, list_of_words, number_of_parameters):
        """
        Allow the player to drop an item in the room.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False
        
        player = game.player
        item_name = list_of_words[1]
        
        # Check if the item exists in the inventory
        if item_name not in player.inventory:
            print(f"\nL'objet '{item_name}' n'est pas dans l'inventaire.\n")
            return False
        
        # Drop the item
        item = player.inventory.pop(item_name)
        player.current_room.inventory[item_name] = item
        print(f"\nVous avez déposé l'objet '{item_name}'.\n")
        return True

    def check(game, list_of_words, number_of_parameters):
        """
        Display the player's inventory.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
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
        Advance NPCs by one step (manual 'wait' command).

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command succeeded, False otherwise.
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
        Allow the player to speak to a character in the room.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        # Allow composite names (multiple words) for the NPC:
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room
        target_name = " ".join(list_of_words[1:])
        
        # Check if the character exists in the room
        character = room.characters.get(target_name, None)
        if character is None:
            print(f"\nIl n'y a pas de personnage nommé '{target_name}' ici.\n")
            return False
        
        # Display the character's message
        print(character.get_msg())
        return True

    def accuse(game, list_of_words, number_of_parameters):
        """
        Allow the player to accuse a character of the crime.
        Can only be done by talking to the Policier at the Police Station.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        if l < 2:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room
        accused_name = " ".join(list_of_words[1:])
        
        # Check if player is at the Police Station
        if room.name != "Commissariat":
            print("\nVous devez aller au commissariat pour accuser quelqu'un.\n")
            return False
        
        # Check if the Policier is in the room
        if "Policier" not in room.characters:
            print("\nLe policier n'est pas ici.\n")
            return False
        
        # Record the accusation
        game.accused = accused_name
        
        # Check if it's the correct person
        if accused_name.lower() == "durand":
            print(f"\nVous avez accusé {accused_name}.")
            print("Le policier l'arrête immédiatement.\n")
        else:
            print(f"\nVous avez accusé {accused_name}.")
            print("Le policier vous regarde avec incrédulité.")
            print("Les preuves ne correspondent pas à cette accusation.\n")
        
        return True

    def analyze(game, list_of_words, number_of_parameters):
        """
        Allow the player to analyze an item at the laboratory.
        Can only be done with the Scientifique at the Labo du commissariat.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG1.format(command_word=command_word))
            return False

        player = game.player
        room = player.current_room
        item_name = list_of_words[1]
        
        # Check if player is at the Laboratory
        if room.name != "Labo du commissariat":
            print("\nVous devez aller au labo du commissariat pour analyser les objets.\n")
            return False
        
        # Check if the Scientifique is in the room
        if "Scientifique" not in room.characters:
            print("\nLe scientifique n'est pas ici.\n")
            return False
        
        # Check if the item is in player's inventory
        if item_name not in player.inventory:
            print(f"\nVous n'avez pas l'objet '{item_name}' dans votre inventaire.\n")
            return False
        
        # Check if it's an item that needs to be analyzed
        if item_name not in game.required_items:
            print(f"\nCet objet n'a pas besoin d'être analysé.\n")
            return False
        
        # Mark the item as analyzed
        if item_name not in game.analyzed_items:
            game.analyzed_items.add(item_name)
            print(f"\n✓ Vous avez analysé: {item_name}")
            print(f"Objets analysés: {len(game.analyzed_items)}/{len(game.required_items)}\n")
        else:
            print(f"\nCet objet a déjà été analysé.\n")
        
        return True

    def quests(game, list_of_words, number_of_parameters):
        """
        Display the list of available quests and remaining time.

        Parameters:
            game (Game): The game object.
            list_of_words (list): The list of words from the command.
            number_of_parameters (int): The number of expected parameters.

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        l = len(list_of_words)
        if l != number_of_parameters + 1:
            command_word = list_of_words[0]
            print(MSG0.format(command_word=command_word))
            return False
        
        # Calculate remaining time
        total_moves = 40
        remaining_moves = total_moves - game.displacement_count
        total_days = 4
        remaining_days = (remaining_moves / total_moves) * total_days
        
        print("\n" + "="*60)
        print("TEMPS IMPARTI POUR L'ENQUÊTE")
        print("="*60)
        print(f"Temps total disponible: {total_days} jours = {total_moves} déplacements")
        print(f"Temps écoulé: {game.displacement_count}/{total_moves} déplacements")
        print(f"Temps restant: {remaining_moves}/{total_moves} déplacements ≈ {remaining_days:.1f} jours")
        print("="*60)
        
        print("\nQUÊTES ACTIVES/DISPONIBLES:\n")
        
        # Display chronological quests
        for i, quest in enumerate(game.quest_manager.quests, 1):
            if i <= 8:  # Chronological quests
                status = "✓" if quest.is_completed else "○"
                if quest.is_completed:
                    active = "\033[92mFINISHED\033[0m"  # Green
                elif quest.is_active:
                    active = "\033[91mACTIVE\033[0m"  # Red
                else:
                    active = "\033[94mINACTIVE\033[0m"  # Blue
                print(f"{status} Quest {i}: {quest.title} ({active})")
                print(f"   Description: {quest.description}")
                if quest.objectives:
                    print(f"   Objectifs: {', '.join(quest.objectives)}")
                print()
        
        print("\nQUÊTES OPTIONNELLES (non-chronologiques):\n")
        
        # Display non-chronological quests
        for i, quest in enumerate(game.quest_manager.quests, 1):
            if i > 8:  # Non-chronological quests
                status = "✓" if quest.is_completed else "○"
                if quest.is_completed:
                    active = "\033[92mFINISHED\033[0m"  # Green
                elif quest.is_active:
                    active = "\033[91mACTIVE\033[0m"  # Red
                else:
                    active = "\033[94mINACTIVE\033[0m"  # Blue
                print(f"{status} {quest.title} ({active})")
                print(f"   Description: {quest.description}")
                if quest.objectives:
                    print(f"   Objectifs: {', '.join(quest.objectives)}")
                print()
        
        print("PROGRÈS D'ANALYSE:")
        print(f"Objets analysés: {len(game.analyzed_items)}/{len(game.required_items)}")
        if game.analyzed_items:
            print(f"Analysés: {', '.join(game.analyzed_items)}")
        missing = game.required_items - game.analyzed_items
        if missing:
            print(f"Objets restants à analyser: {len(missing)}")
        print("="*60 + "\n")
        
        return True