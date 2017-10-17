from main import *
from ocean import *
from player import *
from ship import *


class Square():

    hit_count = 0
    associated_class = None

    def __init__(self, ship_instance):
        self.associated_class = ship_instance

    def was_hit(self):
        self.hit_count = 1
        self.handle_hit()

    def handle_hit(self):
        if isinstance("Ship"):
            self.associated_class.decrement_hp()
