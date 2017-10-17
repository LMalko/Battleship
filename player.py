from main import *
from ocean import *
from ship import *
from square import *
from game_flow import GameFlow


class Player(GameFlow):
    "Abstract Player class."
    ships = {}
    board = None  # Ocean object
    name = "Noname"

    def perform_hit(self, opponent, coordinates):
        pass

    def choose_ships_placement(self, this_players_plan):
        pass


class Human(Player):
    """This is User-Player class."""

    def __init__(self, name):
        self.name = name


class AI(Player):
    """This is AI-Player class."""
    name = "AI"
