from main import *
from ocean import *
from player import *
from ship import *


class Square():

    hit_count = 0
    associated_class = None

    def __init__(self, ship):
        pass

    def was_hit(self):
        self.hit_count = 1
        handle_hit()

    def handle_hit(self):
        if 
