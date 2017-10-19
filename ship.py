
class Ship():

    def decrement_hp(self):
        self.hit_points -= 1

    def __str__(self):
        longest_ship_type_name_plus_margin = 15
        ship_type = self.__class__.__name__.ljust(longest_ship_type_name_plus_margin)

        not_hit_ship = '⛵ '*self.hit_points
        hit_ship = '✖ '*(self.max_hit_points - self.hit_points)
        navy_state = "| {}{}".format(not_hit_ship, hit_ship).ljust(longest_ship_type_name_plus_margin)

        return ship_type + navy_state


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
