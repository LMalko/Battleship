from ship import *
import os

class Square():

    hit_count = 0
    associated_class = None

    def __init__(self, ship_instance=None):

        self.associated_class = ship_instance
        self.single_square_hit_count = 0

    def was_hit(self):

        Square.hit_count += 1
        # if self.single_square_hit_count == 0:
        return self.__handle_hit()     #tu return self.__handle() czyli message

    def __handle_hit(self):  #zamiast printów sychy str i wtedy nie ma problemu z niemożnością importu board_len z Playera
        
        if isinstance(self.associated_class, Ship) and self.single_square_hit_count == 0:
            self.associated_class.decrement_hp()
            if self.associated_class.hit_points == 0:
                self.single_square_hit_count = 1
                return "hit! {} was sunk {} {}!".format(self.associated_class.__class__.__name__)
            else:
                self.single_square_hit_count = 1
                return "hit!"
            
        elif self.single_square_hit_count == 0:
            self.single_square_hit_count = 1
            return "miss!"
        else:
            return "you've already been here before. Nothing special happened..."

    def __str__(self):
        if not self.associated_class:
            if self.single_square_hit_count == 0:
                return " "
            else:
                return '.'
        elif self.single_square_hit_count > 0:
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
