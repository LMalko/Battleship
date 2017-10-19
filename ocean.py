from ship import *
from square import *
import sys


class Ocean():

    def __init__(self, ship_coordinates_dict, ocean_fields):
        self.ship_coordinates_dict = ship_coordinates_dict
        self.ocean_fields = ocean_fields
        # List of references to players ship objects.
        self.my_navy = []
        self.__set_ships_on_board()

    def __set_ships_on_board(self):
        x_coordinate_index = 0
        y_coordinate_index = 1

        for ship_type in self.ship_coordinates_dict.keys():
            ship_object = getattr(sys.modules[__name__], ship_type)()
            self.my_navy.append(ship_object)
            for coordinate_pair in self.ship_coordinates_dict[ship_type]:
                x_coord = coordinate_pair[x_coordinate_index]
                y_coord = coordinate_pair[y_coordinate_index]
                # Access the already initialized Square object.
                square_obj = self.ocean_fields[x_coord][y_coord]
                # Update its class object reference with that of our current ship object.
                square_obj.associated_class_obj = ship_object

    def __str__(self):
        first_row_index = 0

        side_bar_elements = "ABCDEFGHIJ"
        title_bar = ' '
        for element in range(len(self.ocean_fields[first_row_index])):
            # If element is composed of less than two numbers.
            if element + 1 < 10:
                # Increment index by one to start from 1 not from 0.
                title_bar += '|  {}  '.format(element+1)
            # If element is composed of more than two numbers.
            else:
                # Increment index by one to start from 1 not from 0.
                title_bar += '|  {} '.format(element+1)

        separator = '-'*len(title_bar) + '\n'
        # ;)
        super_str = ''
        super_str += title_bar + '\n' + separator

        for row_index in range(len(self.ocean_fields)):
            super_str += side_bar_elements[row_index]
            for column_index in range(len(self.ocean_fields[row_index])):
                super_str += "|  {}  ".format(self.ocean_fields[row_index][column_index].__str__())
            super_str += '\n'
            super_str += separator

        return(super_str)
