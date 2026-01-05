"""Classe principale du jeu.

Fichier `game.py` : organisation principale du jeu, initialisation des salles,
des commandes, des objets et des personnages.
"""

# Import des modules
from room import Room
from player import Player
from command import Command
from actions import Actions
from item import Item
import character

DEBUG = False

class Game:

    # Constructeur
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
        self.history = []
        # Règle du jeu : si False, Durand n'a pas le droit d'être au Commissariat
        self.law_allows_durand_commissariat = False
        # Pistes et score de suspicion par PNJ
        self.clues = []
        self.suspicions = {}
        # Nombre de façons de résoudre le mystère (méthodes alternées)
        self.resolution_methods = 2
    
    # Configuration du jeu
    def setup(self):

        # Déclaration des commandes
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
        talk = Command("talk", " <nom> : parler à un personnage", Actions.talk, 1)
        self.commands["talk"] = talk
        # Note: commande 'wait' retirée — les PNJ avancent automatiquement
        # après chaque commande du joueur (ancienne structure restaurée).
        
        # Création des salles
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
        

        # Création des sorties entre salles
        Rue_Montfleur.exits = {"E": Maison_crime, "N": Durand, "S": Lenoir, "O": Café}
        Maison_crime.exits = {"O": Rue_Montfleur, "U": Grenier, "D": Cave, "E": Jardin}
        Durand.exits = {"S": Rue_Montfleur, "O": Café}
        Lenoir.exits = {"N": Rue_Montfleur, "S": Parc}
        Café.exits = {"E": Rue_Montfleur, "N": Commissariat}
        Commissariat.exits = {"S": Café,"E": Morgue}
        Parc.exits = {"N": Lenoir, "E": Bibliotheque}
        Bibliotheque.exits = {"O": Parc}
        Grenier.exits = {"D": Maison_crime}
        Cave.exits = {"U": Maison_crime}
        Jardin.exits = {"O": Maison_crime}
        Morgue.exits = {"O": Commissariat}

        # Initialisation du joueur et salle de départ
        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Maison_crime
        self.player.history.append(self.player.current_room)

        # Ajout des objets dans les salles (conformes aux descriptions)
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

        # Setup characters (PNJ)
        durand_pnj = character.Character("Durand", "un voisin nerveux", Durand,
                               ["Je n'ai rien vu !", "Pourquoi me soupçonner ?", "Je vous ai déjà dit la vérité."])
        # Définir les salles autorisées pour Durand : sa maison, la rue, la Maison du crime et le Commissariat
        durand_pnj.allowed_rooms = [Durand, Rue_Montfleur, Maison_crime, Commissariat]
        Durand.characters["Durand"] = durand_pnj

        lenoir_pnj = character.Character("Lenoir", "une vieille dame mystérieuse", Lenoir,
                               ["J'ai entendu un bruit...", "Je crois avoir vu une silhouette.", "Tout cela est étrange..."])
        Lenoir.characters["Lenoir"] = lenoir_pnj

        policier = character.Character("Policier", "un enquêteur du commissariat", Commissariat,
                             ["Apportez-moi des preuves.", "Je peux analyser vos indices.", "La vérité finira par éclater."])
        Commissariat.characters["Policier"] = policier

        # PNJ à la morgue: médecin légiste fournissant analyses et autopsies
        medecin_legiste = character.Character("Médecin légiste", "un médecin légiste studieux", Morgue,
                               [
                                "Rapport préliminaire: sur la scène du crime j'ai observé une blessure pénétrante, du sang et un couteau trouvé sur place (voir 'knife' dans la Maison du crime).",
                                "Autopsie: la cause du décès semble être une plaie thoracique. L'angle et la profondeur indiquent une attaque rapprochée; peu de signes de défense.",
                                "Éléments identifiés: une clé ('key') retrouvée chez Durand, une lettre ('letter') chez Madame Lenoir, et des photos ('photos') dans le grenier. Ces objets doivent être analysés en laboratoire.",
                                "Analyse circonstancielle: Durand s'est montré nerveux, Lenoir a entendu un bruit, et le Policier centralise les preuves au Commissariat. L'arme ('knife' ou 'weapon') reste un élément clé.",
                                "Conclusion et recommandations: la victime a été attaquée sur place. Prélevez et apportez‑moi l'arme pour des traces, vérifiez le Jardin et le Grenier pour d'autres indices, et interrogez à nouveau les témoins."
                               ])
        Morgue.characters["Médecin légiste"] = medecin_legiste

    def play(self):
        self.setup()
        self.print_welcome()
        # Loop until the game is finished
        while not self.finished:
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
            # Restaurer l'ancien comportement : après chaque commande joueur,
            # tenter de déplacer les PNJ et afficher leurs déplacements.
            # Ne pas appeler si la partie est terminée.
            if not self.finished:
                try:
                    self.update_characters()
                except Exception:
                    # Ne pas casser le jeu si l'actualisation plante.
                    pass

    def update_characters(self):
        """
        Tente de déplacer tous les PNJ et affiche des notifications
        si un PNJ part ou arrive dans la salle du joueur.
        Appeler après execution d'une commande joueur.
        """
        moved_events = []  # tuples (character, old_room, new_room)

        # Construire un snapshot de tous les personnages présents au début
        all_characters = []
        for room in self.rooms:
            for character in list(room.characters.values()):
                all_characters.append(character)

        # Éviter de traiter deux fois le même objet (par sécurité)
        seen = set()
        for character in all_characters:
            if id(character) in seen:
                continue
            seen.add(id(character))
            old_room = character.current_room
            moved = character.move()
            # N'afficher True/False et messages détaillés que pour Durand
            if character.name == "Durand":
                print(f"\n{character.name} moved? {moved}")
                if moved:
                    if character.current_room is not old_room:
                        new_room = character.current_room
                        print(f"{character.name} a quitté '{old_room.name}' et est allé à '{new_room.name}'.")
                    else:
                        print(f"{character.name} a tenté de se déplacer mais reste dans '{old_room.name}'.")
                else:
                    print(f"{character.name} n'a pas bougé (reste dans '{old_room.name}').")
            # Conserver la collecte d'événements pour traitement ultérieur
            if moved and character.current_room is not old_room:
                new_room = character.current_room
                moved_events.append((character, old_room, new_room))

        # Les mouvements sont loggés dans `Character.move()` via DEBUG.
        # On évite d'envoyer des notifications textuelles supplémentaires ici
        # pour que la gestion/notification au joueur soit effectuée ailleurs.
        # Traiter les événements de déplacement pour produire des indices/suspicion
        for (ch, old_room, new_room) in moved_events:
            # Exemple de règle spécifique pour Durand
            if ch.name == "Durand":
                # Durand aperçu au Commissariat
                if new_room.name == "Commissariat":
                    # Si Durand est au Commissariat alors que la loi l'interdit,
                    # on n'imprime pas directement le message : on crée un item-indice
                    # que le joueur devra trouver en regardant la pièce.
                    if not self.law_allows_durand_commissariat:
                        self.suspicions["Durand"] = self.suspicions.get("Durand", 0) + 1
                        clue_text = "Il est parti malgré l'interdiction : Durand a demandé des infos sur l'enquête."
                        clue_item = Item("indice_durand_commissariat", clue_text, 0)
                        # déposer l'indice dans la nouvelle salle pour que le joueur le découvre
                        new_room.inventory[clue_item.name] = clue_item
                        # garder en mémoire mais ne pas afficher automatiquement
                        self.clues.append(clue_text)
                    else:
                        clue_text = "Durand vu au Commissariat, il a discuté de l'enquête."
                        clue_item = Item("indice_durand_commissariat", clue_text, 0)
                        new_room.inventory[clue_item.name] = clue_item
                        self.clues.append(clue_text)
                # Si Durand se retrouve ailleurs que ses salles habituelles, on note aussi
                elif ch.allowed_rooms is not None and new_room not in ch.allowed_rooms:
                    # Déposer un indice dans la pièce inattendue
                    self.suspicions["Durand"] = self.suspicions.get("Durand", 0) + 1
                    clue_text = f"On a retrouvé Durand ici : {new_room.name}. C'est inattendu et cela augmente la suspicion."
                    clue_item = Item("indice_durand_inattendu", clue_text, 0)
                    new_room.inventory[clue_item.name] = clue_item
                    self.clues.append(clue_text)

    # Print the welcome message
    def print_welcome(self):     
        print(f"\nBienvenue {self.player.name} dans Crime à Montfleur !")
        print("Entrez 'help' si vous avez besoin d'aide.\n")

    # Scénario d’introduction
        print("Une nuit sombre vient de tomber sur Montfleur...")
        print("Un crime mystérieux a été commis dans une maison de la rue principale.")
        print("Les voisins murmurent, les témoins hésitent, et les preuves semblent se cacher dans chaque recoin.")
        print("Votre mission : explorer les lieux, interroger les habitants, et découvrir la vérité.\n")
 
    # Description de la salle de départ
        print(self.player.current_room.get_long_description())
    

def main():
    # Create a game object and play the game
    Game().play()
    

if __name__ == "__main__":
    main()
