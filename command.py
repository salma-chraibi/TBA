"""
Classe `Command`.

Cette classe représente une commande du jeu composée d'un mot-clé, d'une aide, d'une action callable
et du nombre de paramètres attendus.

Attributs:
    command_word (str): Le mot de la commande.
    help_string (str): La chaîne d'aide affichée.
    action (callable): La fonction appelée pour exécuter la commande.
    number_of_parameters (int): Le nombre de paramètres attendus.

Exemple:
    >>> from actions import go
    >>> command = Command("go", "Permet de se déplacer dans une direction.", go, 1)
    >>> command.command_word
    'go'
"""

class Command:
    def __init__(self, command_word, help_string, action, number_of_parameters):
        self.command_word = command_word
        self.help_string = help_string
        self.action = action
        self.number_of_parameters = number_of_parameters

    def __str__(self):
        return self.command_word + self.help_string


