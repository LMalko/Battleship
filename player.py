from main import *
from ocean import *
from ship import *
from square import *


class Player(GameFlow):
    
    ships_plan: {}
    board = None
    name = "Noname"

    def __init__(self, ship_instance):

        self.name = ship_instance

    def perform_hit(self, opponent_instance, coordinates):

        self.board = coordinates

    def choose_ships_placement(self, this_players_plan):
        
        self.ships_plan = this_players_plan
