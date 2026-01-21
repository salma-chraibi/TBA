"""Main game class.

File `game.py`: main organization of the game, initialization of rooms,
commands, objects, and characters.
"""

# Import modules
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
from quest import Quest
import character

DEBUG = False

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []
        # Game rule: if False, Durand is not allowed to be at the Police Station
        self.law_allows_durand_commissariat = False
        # Clues and suspicion score per NPC
        self.clues = []
        self.suspicions = {}
        # Number of ways to solve the mystery (alternate methods)
        self.resolution_methods = 2
        # Quest management
        from quest import Quest, QuestManager
        self.quest_manager = QuestManager()
        # Displacement counter (excluding certain rooms)
        self.displacement_count = 0
        # Analyzed items
        self.analyzed_items = set()
        # Items to analyze: key, photos, chest, knife, weapon, letter
        self.required_items = {"key", "photos", "chest", "knife", "weapon", "letter"}
        # Accused person
        self.accused = None
        # Track visited crime scene rooms for Quest 1
        self.visited_crime_scene_rooms = set()
        # Track collected items for Quest 1
        self.collected_items = set()
    
    # Game setup
    def setup(self):

        # Declare commands
        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        back = Command("back", " : revenir à la pièce précédente", Actions.back, 0)
        self.commands["back"] = back
        history = Command("history", " : afficher l'historique des pièces visitées", Actions.history, 0)
        self.commands["history"] = history
        look = Command("look", " : observer l'environnement", Actions.look, 0)
        self.commands["look"] = look
        take = Command("take", " <objet> : prendre un objet", Actions.take, 1)
        self.commands["take"] = take
        drop = Command("drop", " <objet> : déposer un objet", Actions.drop, 1)
        self.commands["drop"] = drop
        check = Command("check", " : vérifier l'inventaire", Actions.check, 0)
        self.commands["check"] = check
        talk = Command("talk", " <name> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        accuse = Command("accuse", " <name> : accuser un personnage du crime", Actions.accuse, 1)
        self.commands["accuse"] = accuse
        analyze = Command("analyze", " <item> : analyser un objet au labo", Actions.analyze, 1)
        self.commands["analyze"] = analyze
        quests = Command("quests", " : afficher vos quêtes disponibles et le temps restant", Actions.quests, 0)
        self.commands["quests"] = quests
        # Note: 'wait' command removed — NPCs advance automatically
        # after each player command (old structure restored).
        
        # Create rooms
        Rue_Montfleur = Room("Rue de Montfleur", "dans la rue de Montfleur. Il y a des accès vers les maisons voisines et des traces de pneus.")
        self.rooms.append(Rue_Montfleur)

        Maison_crime = Room("Maison du crime", "dans la maison du crime. Il y a des traces de lutte et une atmosphère pesante.")
        self.rooms.append(Maison_crime)

        Durand = Room("Maison de Durand", "dans la maison de Durand. Il y a une clé suspecte et des vêtements tachés.")
        self.rooms.append(Durand)

        Lenoir = Room("Maison de Madame Lenoir", "dans la maison de Madame Lenoir. Il y a une lettre mystérieuse et une fenêtre donnant sur la rue.")
        self.rooms.append(Lenoir)

        Café = Room("Café du Marchand", "Vous êtes dans le café du Marchand. Il y a des rumeurs qui circulent et un carnet d’habitudes des voisins.")
        self.rooms.append(Café)

        Commissariat = Room("Commissariat", "dans le commissariat. Il y a un policier prêt à analyser les preuves.")
        self.rooms.append(Commissariat)

        Parc = Room("Parc de Montfleur", "dans le parc de Montfleur. Il y a un témoin qui dit avoir vu une silhouette.")
        self.rooms.append(Parc)
 
        Bibliotheque = Room("Bibliothèque", "dans la bibliothèque. Il y a des archives poussiéreuses et des livres anciens.")
        self.rooms.append(Bibliotheque)
 
        Grenier = Room("Grenier", "dans le grenier de la maison du crime. Il y a des vieilles photos et une malle poussiéreuse.")
        self.rooms.append(Grenier)
 
        Cave = Room("Cave", "dans la cave de la maison du crime. Il y a des cartons humides et un coffre verrouillé.")
        self.rooms.append(Cave)
 
        Jardin = Room("Jardin", "dans le jardin de la maison du crime. Il y a des buissons épais et une arme dissimulée.")
        self.rooms.append(Jardin)

        Morgue = Room("Morgue de Montfleur","dans la morgue de Montfleur. L’air est glacial, des corps reposent sous des draps blancs, et une odeur de formol flotte.")
        self.rooms.append(Morgue)
        
        Labo = Room("Labo du commissariat", "dans le laboratoire de la police. Des équipements d'analyse et des résultats de tests sont visibles sur les tables.")
        self.rooms.append(Labo)
        

        # Création des sorties entre salles
        Rue_Montfleur.exits = {"E": Maison_crime, "N": Durand, "S": Lenoir, "O": Café}
        Maison_crime.exits = {"O": Rue_Montfleur, "U": Grenier, "D": Cave, "E": Jardin}
        Durand.exits = {"S": Rue_Montfleur, "O": Café}
        Lenoir.exits = {"N": Rue_Montfleur, "S": Parc}
        Café.exits = {"E": Rue_Montfleur, "N": Commissariat}
        Commissariat.exits = {"S": Café, "E": Morgue, "O": Labo}
        Parc.exits = {"N": Lenoir, "E": Bibliotheque}
        Bibliotheque.exits = {"O": Parc}
        Grenier.exits = {"D": Maison_crime}
        Cave.exits = {"U": Maison_crime}
        Jardin.exits = {"O": Maison_crime}
        Morgue.exits = {"O": Commissariat}
        Labo.exits = {"E": Commissariat}

        # Initialize player and starting room
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Maison_crime
        self.player.history.append(self.player.current_room)

        # Create quests
        quest1 = Quest("Inspecter la maison du crime", 
                      "Inspecter toutes les pièces de la maison du crime (Grenier, Maison, Sous-Sol, Jardin) et trouvez des indices",
                      ["Visiter le Grenier", "Visiter le Sous-Sol (Cave)", "Visiter le Jardin", "Récupérer les indices"],
                      "Nouvelles pistes découvertes")
        quest1.activate()
        self.quest_manager.add_quest(quest1)

        quest2 = Quest("Faire analyser les objets au Labo",
                      "Faire analyser les objets trouvés à la maison du crime au Labo du commissariat",
                      ["Accéder au Labo du commissariat", "Parler au scientifique", "Faire analyser chaque objet"],
                      "Résultats d'analyse importants")
        self.quest_manager.add_quest(quest2)

        quest3 = Quest("Aller à la morgue",
                      "Aller à la morgue pour parler au médecin légiste",
                      ["Se rendre à la morgue", "Parler au Médecin légiste", "Récupérer le rapport d'autopsie"],
                      "Indices sur la cause du décès")
        self.quest_manager.add_quest(quest3)

        quest4 = Quest("Explorer les environs",
                      "Explorez les environs et cherchez des indices et des personnes à qui parler",
                      ["Visiter le Parc", "Visiter le Café", "Interroger les témoins"],
                      "Témoignages importants")
        self.quest_manager.add_quest(quest4)

        quest5 = Quest("Inspecter chez Mme Lenoir",
                      "Inspectez la maison de Mme Lenoir et interrogez-la",
                      ["Visiter la maison de Lenoir", "Fouiller la maison", "Parler à Mme Lenoir"],
                      "Découvertes chez Lenoir")
        self.quest_manager.add_quest(quest5)

        quest6 = Quest("Analyser les objets chez Lenoir",
                      "Faire analyser les objets trouvés chez Lenoir au commissariat",
                      ["Apporter les objets au commissariat", "Faire analyser la lettre", "Obtenir les résultats"],
                      "Preuves contre le meurtrier")
        self.quest_manager.add_quest(quest6)

        quest7 = Quest("Inspecter chez Durand",
                      "Inspectez chez Durand puis trouvez-le et interrogez-le",
                      ["Visiter la maison de Durand", "Fouiller la maison", "Trouver Durand", "L'interroger"],
                      "Aveux du meurtrier")
        self.quest_manager.add_quest(quest7)

        quest8 = Quest("Résoudre l'énigme",
                      "Essayez de trouver des nouveaux indices sinon accusez celui que vous pensez être le meurtrier",
                      ["Réunir tous les indices", "Analyser les preuves", "Accuser le coupable"],
                      "Fin de l'enquête")
        self.quest_manager.add_quest(quest8)

        # Non-chronological quests
        quest9 = Quest("Ouvrir le coffre",
                      "Ouvrir le coffre avec la clé mystérieuse",
                      ["Trouver la clé", "Récupérer le coffre", "Ouvrir le coffre"],
                      "Secrets du coffre")
        self.quest_manager.add_quest(quest9)

        quest10 = Quest("Lire la lettre mystérieuse",
                       "Ouvrir et lire la lettre mystérieuse",
                       ["Trouver la lettre", "Récupérer la lettre", "Lire la lettre"],
                       "Révélations de la lettre")
        self.quest_manager.add_quest(quest10)

        # Add objects to rooms (conforming to descriptions)
        knife = Item("knife", "un couteau ensanglanté", 0.5)
        Maison_crime.inventory["knife"] = knife

        key = Item("key", "une clé suspecte", 0.2)
        Durand.inventory["key"] = key

        letter = Item("letter", "une lettre mystérieuse", 0.001)
        Lenoir.inventory["letter"] = letter

        chest = Item("chest", "un coffre verrouillé", 5)
        Cave.inventory["chest"] = chest

        photos = Item("photos", "des vieilles photos", 0.5)
        Grenier.inventory["photos"] = photos

        weapon = Item("weapon", "une arme dissimulée", 3)
        Jardin.inventory["weapon"] = weapon

        # Add useless clues
        city_book = Item("city_book", "un livre décrivant l'histoire de la ville", 0.8)
        Bibliotheque.inventory["city_book"] = city_book

        # Setup characters (NPCs)
        durand_pnj = character.Character("Durand", "un voisin nerveux", Durand,
                               ["Je n'ai rien vu !", "Pourquoi me soupçonner ?", "Je vous ai déjà dit la vérité."])
        # Define authorized rooms for Durand: his house, the street, the Crime House, and the Police Station
        durand_pnj.allowed_rooms = [Durand, Rue_Montfleur, Maison_crime, Commissariat]
        Durand.characters["Durand"] = durand_pnj

        lenoir_pnj = character.Character("Lenoir", "une vieille dame mystérieuse", Lenoir,
                               ["J'ai entendu un bruit...", "Je crois avoir vu une silhouette.", "Tout cela est étrange..."])
        Lenoir.characters["Lenoir"] = lenoir_pnj

        policier = character.Character("Policier", "un enquêteur du commissariat", Commissariat,
                             ["Apportez-moi des preuves.", "Vous devez analyser ces 6 objets: clé, photos, coffre, couteau, arme, lettre.", "Les indices pointent vers Durand - accusez-le quand vous serez sur!", "La vérité finira par éclater."])
        Commissariat.characters["Policier"] = policier

        # NPC at the morgue: medical examiner providing analysis and autopsies
        medecin_legiste = character.Character("Médecin légiste", "un médecin légiste studieux", Morgue,
                               [
                                "Rapport préliminaire: sur la scène du crime j'ai observé une blessure pénétrante, du sang et un couteau trouvé sur place (voir 'knife' dans la Maison du crime).",
                                "Autopsie: la cause du décès semble être une plaie thoracique. L'angle et la profondeur indiquent une attaque rapprochée; peu de signes de défense.",
                                "ELEMENTS A ANALYSER (6 OBJETS): clé ('key'), photos ('photos'), coffre ('chest'), couteau ('knife'), arme ('weapon'), lettre ('letter'). Tous ces objets doivent être apportés au laboratoire pour analyse complète.",
                                "Analyse circonstancielle: Durand s'est montré nerveux et s'est déplacé - il a quitté 'Maison de Durand' et est allé à 'Rue de Montfleur'. Lenoir a entendu un bruit, et le Policier centralise les preuves. Durand est notre suspect principal.",
                                "COUPABLE PROBABLE: Durand! Voici pourquoi: nervosité suspecte, possession de la clé, et ses déplacements coïncident avec l'heure du crime. Les preuves l'incriminent fortement.",
                                "Conclusion et recommandations: la victime a été attaquée sur place. Accusez Durand au commissariat une fois que vous aurez recueilli toutes les preuves."
                               ])
        Morgue.characters["Médecin légiste"] = medecin_legiste

        # NPC at the laboratory: scientist for analyzing evidence
        scientifique = character.Character("Scientifique", "un scientifique du labo", Labo,
                               [
                                "Bienvenue au laboratoire. Vous devez analyser 6 objets essentiels: clé, photos, coffre, couteau, arme, et lettre.",
                                "J'ai tous les équipements nécessaires pour tester ces preuves et révéler la vérité.",
                                "Une fois tous les objets analysés, vous aurez suffisamment de preuves pour accuser le meurtrier.",
                                "Les résultats montrent que Durand est impliqué - allez l'accuser au commissariat!"
                               ])
        Labo.characters["Scientifique"] = scientifique

    def win(self):
        """
        Check if the player has won the game.
        Win condition: Accuse Durand, have all items, analyzed all items, within 4 days (40 moves).
        
        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check if all required items are analyzed
        if self.required_items != self.analyzed_items:
            return False
        
        # Check if player accused someone
        if self.accused is None:
            return False
        
        # Check if accused the right person (Durand)
        if self.accused.lower() != "durand":
            return False
        
        # Check if within time limit (40 moves)
        if self.displacement_count > 40:
            return False
        
        return True

    def loose(self):
        """
        Check if the player has lost the game.
        Lose condition: Accuse wrong person, missing items, not analyzed, or over 4 days.
        
        Returns:
            bool: True if the player has lost, False otherwise.
        """
        # Check if exceeded time limit
        if self.displacement_count > 40:
            return True
        
        # Check if accused someone wrong
        if self.accused is not None and self.accused.lower() != "durand":
            return True
        
        return False
    
    def check_quest1_completion(self):
        """
        Check if Quest 1 should be completed.
        Quest 1 is complete when player has visited all crime scene rooms and collected all items.
        """
        required_rooms = {"Grenier", "Maison du crime", "Cave", "Jardin"}
        required_items = {"photos", "knife", "chest", "weapon"}
        
        if self.visited_crime_scene_rooms == required_rooms and self.collected_items == required_items:
            quest1 = self.quest_manager.get_quest_by_title("Inspecter la maison du crime")
            if quest1 and not quest1.is_completed:
                quest1.complete_quest(self.player)

    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
            # Check loose condition
            if self.loose():
                print("\nVOUS AVEZ PERDU!")
                if self.displacement_count > 40:
                    print(f"Vous avez dépassé les 4 jours d'investigation ({self.displacement_count} déplacements).")
                elif self.accused and self.accused.lower() != "durand":
                    print(f"Vous avez accusé la mauvaise personne: {self.accused}")
                else:
                    print("Vous n'avez pas tous les indices ou vous ne les avez pas analysés.")
                self.finished = True
                break
            
            # Check win condition
            if self.win():
                print("\nVOUS AVEZ GAGNÉ!")
                print(f"Vous avez résolu l'énigme en {self.displacement_count} déplacements!")
                print("Durand a été arrêté et sera jugé pour ses crimes.")
                self.finished = True
                break
            
            # Get the command from the player
            self.process_command(input("> "))    
        return None

    # Process the command entered by the player
    def process_command(self, command_string) -> None:

        # Split the command string into a list of words
        list_of_words = command_string.split(" ")

        command_word = list_of_words[0]

        if command_string.strip() == "":
            return
        # If the command is not recognized, print an error message
        if command_word not in self.commands.keys():
            print(f"\nCommande non reconnue. Tapez 'help' pour voir la liste des commandes disponibles.\n")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)
            # Restore the old behavior: after each player command,
            # attempt to move NPCs and display their movements.
            # Do not call if the game is finished.
            if not self.finished:
                try:
                    self.update_characters()
                except Exception:
                    # Do not break the game if the update crashes.
                    pass

    def update_characters(self):
        """
        Attempt to move all NPCs and display notifications
        if an NPC leaves or arrives in the player's room.
        Call after execution of a player command.
        """
        moved_events = []  # tuples (character, old_room, new_room)

        # Build a snapshot of all characters present at the start
        all_characters = []
        for room in self.rooms:
            for character in list(room.characters.values()):
                all_characters.append(character)

        # Avoid processing the same object twice (for safety)
        seen = set()
        for character in all_characters:
            if id(character) in seen:
                continue
            seen.add(id(character))
            old_room = character.current_room
            moved = character.move()
            # Keep collecting events for later processing
            if moved and character.current_room is not old_room:
                new_room = character.current_room
                moved_events.append((character, old_room, new_room))

        # Movements are logged in `Character.move()` via DEBUG.
        # We avoid sending additional text notifications here
        # so that player management/notification is done elsewhere.
        # Process movement events to produce clues/suspicion
        for (ch, old_room, new_room) in moved_events:
            # Example of specific rule for Durand
            if ch.name == "Durand":
                # Durand spotted at the Police Station
                if new_room.name == "Commissariat":
                    # If Durand is at the Police Station when the law forbids it,
                    # we don't print the message directly: we create a clue item
                    # that the player must find by looking at the room.
                    if not self.law_allows_durand_commissariat:
                        self.suspicions["Durand"] = self.suspicions.get("Durand", 0) + 1
                        clue_text = "Il est parti malgré l'interdiction : Durand a demandé des infos sur l'enquête."
                        clue_item = Item("indice_durand_commissariat", clue_text, 0)
                        # deposit the clue in the new room so the player discovers it
                        new_room.inventory[clue_item.name] = clue_item
                        # keep in memory but don't display automatically
                        self.clues.append(clue_text)
                    else:
                        clue_text = "Durand vu au Commissariat, il a discuté de l'enquête."
                        clue_item = Item("indice_durand_commissariat", clue_text, 0)
                        new_room.inventory[clue_item.name] = clue_item
                        self.clues.append(clue_text)
                # If Durand ends up elsewhere than his usual rooms, we also note it
                elif ch.allowed_rooms is not None and new_room not in ch.allowed_rooms:
                    # Deposit a clue in the unexpected room
                    self.suspicions["Durand"] = self.suspicions.get("Durand", 0) + 1
                    clue_text = f"Durand was found here: {new_room.name}. This is unexpected and increases suspicion."
                    clue_item = Item("indice_durand_inattendu", clue_text, 0)
                    new_room.inventory[clue_item.name] = clue_item
                    self.clues.append(clue_text)

    # Print the welcome message
    def print_welcome(self):     
        print(f"\nBienvenue {self.player.name} dans Crime à Montfleur !")
        print("Entrez 'help' si vous avez besoin d'aide.\n")

    # Introduction scenario
        print("Une nuit sombre vient de tomber sur Montfleur...")
        print("Un crime mystérieux a été commis dans une maison de la rue principale.")
        print("Les voisins murmurent, les témoins hésitent, et les preuves semblent se cacher dans chaque recoin.")
        print("Votre mission : explorer les lieux, interroger les habitants, et découvrir la vérité.\n")
        
        # Display time limit information
        print("="*60)
        print("CONDITIONS DE L'ENQUÊTE")
        print("="*60)
        print("Temps disponible: 4 jours = 40 déplacements")
        print("(Les déplacements dans le Grenier, Jardin, Cave et Labo ne comptent pas)")
        print()
        print("Tapez 'quests' pour voir vos quêtes et le temps restant")
        print("="*60 + "\n")
 
    # Description of the starting room
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
