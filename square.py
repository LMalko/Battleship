# from main import *
# from ocean import *
# from player import *
from ship import *
# from game_flow import *


class Square():

    hit_count = 0
    associated_class = None

    def __init__(self, ship_instance=None):

        self.associated_class = ship_instance

    def was_hit(self):

        self.hit_count += 1
        if self.hit_count <= 1:
            self.handle_hit()

    def handle_hit(self):   # __handle_hit bo nie ma być wywoływana spoza klasy A.
        
        if isinstance(self.associated_class, Ship):
            self.associated_class.decrement_hp()

    def __str__(self):

        if not self.associated_class:
            return "."
        elif self.hit_count > 0:
            return "X"
        else:
            return "O"
        

# boat = Square(Battleship())
# titanic = Square(Battleship())
# titanic.was_hit()
# water = Square()
# print('boat', boat)
# print('ocean', water)
# print('titanic', titanic)
