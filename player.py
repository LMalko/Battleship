from main import *
from ocean import Ocean
from ship import Destroyer, Submarine, Cruiser, Battleship, Carrier
from square import Square
from game_flow import GameFlow


class Player(GameFlow):
    "Abstract Player class."
    name = "Noname"
    # Player's availible ships:
    ships = [Destroyer, Submarine, Cruiser, Battleship, Carrier]
    my_ships = {}  # containts Player's created ships
    board = None  # Ocean object

    def perform_hit(self, opponent, coordinates):
        pass  # czekam na Anię :)

    def choose_ships_placement(self, this_players_plan):
        pass  # chyba Michał to robi? :)

    def get_my_ships(self):
        self.my_ships = {}  # contains Player's ships
        for ship in self.ships:
            self.my_ships[ship.__name__] = [[1, 2], [3, 4]]  # todo

    # ###### was creating objects - needlessly:
    # def get_my_ships(self):
    #     self.my_ships = {}  # contains Player's ships
    #     for ship in self.ships:
    #         self.my_ships[ship.__name__] = ship()


class Human(Player):
    """This is User-Player class."""

    def __init__(self, name):
        self.name = name
        self.board = "tu będzie ocean"  # Ocean()
        self.get_my_ships()


class AI(Player):
    """This is AI-Player class."""
    name = "AI"
    def __init__(self):
        self.board = "tu będzie ocean"  # Ocean()
        self.get_my_ships()
