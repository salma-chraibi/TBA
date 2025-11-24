# Description: Game class

# Import modules

from room import Room
from player import Player
from command import Command
from actions import Actions

class Game:

    # Constructor
    def __init__(self):
        self.finished = False
        self.rooms = []
        self.commands = {}
        self.player = None
    
    # Setup the game
    def setup(self):

        # Setup commands

        help = Command("help", " : afficher cette aide", Actions.help, 0)
        self.commands["help"] = help
        quit = Command("quit", " : quitter le jeu", Actions.quit, 0)
        self.commands["quit"] = quit
        go = Command("go", " <direction> : se déplacer dans une direction cardinale (N, E, S, O)", Actions.go, 1)
        self.commands["go"] = go
        
        # Setup rooms

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
        

        # Create exits for rooms
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

        # Setup player and starting room

        self.player = Player(input("\nEntrez votre nom: "))
        self.player.current_room = Maison_crime

    # Play the game
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

        # If the command is not recognized, print an error message
        if command_word == "" :
            print("")
        # If the command is recognized, execute it
        else:
            command = self.commands[command_word]
            command.action(self, list_of_words, command.number_of_parameters)

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
