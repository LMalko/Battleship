# from main import *
# from ocean import *
# from player import *
# from square import *


class Ship():
    """Abstract class represents Ships objects."""

    def decrement_hp(self):
        self.hit_points -= 1

    def __str__(self):
        return self.__class__.__name__ + ", HP: " + str(self.hit_points)


class Destroyer(Ship):
    hit_points = 2


class Submarine(Ship):
    hit_points = 3


class Cruiser(Ship):
    hit_points = 3


class Battleship(Ship):
    hit_points = 4


class Carrier(Ship):
    hit_points = 5
