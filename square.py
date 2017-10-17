from main import *
from ocean import *
from player import *
from ship import *
from game_flow import *


class Square():

    hit_count = 0
    associated_class = None

    def __init__(self, ship_instance=None):

        self.associated_class = ship_instance

    def was_hit(self):

        self.hit_count = 1
        self.handle_hit()

    def handle_hit(self):
        
        if isinstance("Ship"):
            self.associated_class.decrement_hp()

    def __str__(self):

        if self.associated_class == None:
            print(".")
        elif self.hit_count > 0:
            print("X")
        else:
            print("O")
        
