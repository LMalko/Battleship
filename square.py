from ship import *

class Square():

    hit_count = 0
    associated_class = None

    def __init__(self, ship_instance=None):

        self.associated_class = ship_instance

    def was_hit(self):

        self.hit_count += 1
        if self.hit_count <= 1:
            self.__handle_hit()

    def __handle_hit(self):
        
        if isinstance(self.associated_class, Ship):
            self.associated_class.decrement_hp()
            if self.associated_class.hit_points == 0:
                print("hit! {} was sunk".format(self.associated_class.__class__.__name__).center(10))
            else:
                print("hit!".center(10))
        else:
            message = "miss!"
            str_len = 10 + len(message)
            print(message.center(str_len))

    def __str__(self):

        if not self.associated_class:
            if self.hit_count == 0:
                return " "
            else:
                return '.'
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
