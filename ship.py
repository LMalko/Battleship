
class Ship():
    """Abstract class represents Ships objects."""

    def decrement_hp(self):
        self.hit_points -= 1

    def __str__(self):
        return self.__class__.__name__ + ", HP: " + '⛵ ' * self.hit_points + '✖ '*(self.max_hit_points - self.hit_points)# str(self.hit_points)


class Destroyer(Ship):
    max_hit_points = 2
    
    def __init__(self):
        self.hit_points = self.max_hit_points


class Submarine(Ship):
    max_hit_points = 3

    def __init__(self):
        self.hit_points = self.max_hit_points


class Cruiser(Ship):
    max_hit_points = 3

    def __init__(self):
        self.hit_points = self.max_hit_points


class Battleship(Ship):
    max_hit_points = 4

    def __init__(self):
        self.hit_points = self.max_hit_points


class Carrier(Ship):
    max_hit_points = 5

    def __init__(self):
        self.hit_points = self.max_hit_points
