from ship import *
from square import *
import sys


class Ocean():

    def __init__(self, ship_coordinates_dict, ocean_fields):
        self.ship_coordinates_dict = ship_coordinates_dict
        self.ocean_fields = ocean_fields
        self.my_navy = []   # list of references to players ship objects
        self.__set_ships_on_board()

    def __set_ships_on_board(self):
        x_coordinant_index = 0
        y_coordinant_index = 1

        for ship_type in self.ship_coordinates_dict.keys():     # ship_type is a string
            ship_object = getattr(sys.modules[__name__], ship_type)()
            self.my_navy.append(ship_object)
            for list_of_coordinants in self.ship_coordinates_dict.get(ship_type):
                for coordinants in range(len(self.ship_coordinates_dict.get(ship_type))):
                    x_coord = list_of_coordinants[x_coordinant_index]
                    y_coord = list_of_coordinants[y_coordinant_index]
                    self.ocean_fields[x_coord].pop(y_coord)
                    self.ocean_fields[x_coord].insert(y_coord, Square(ship_object))


    def __str__(self):
        first_row_index = 0

        side_bar_elements = "ABCDEFGHIJ"
        title_bar = ' '
        for element in range(len(self.ocean_fields[first_row_index])):
            if element + 1 < 10:    # if element is composed of less than two numbers
                title_bar += '|  {}  '.format(element+1)  # increment index by one to start from 1 not from 0
            else:                   # if element is composed of more than two numbers
                title_bar += '|  {} '.format(element+1)   # increment index by one to start from 1 not from 0

        separator = '-'*len(title_bar) + '\n'
        super_str = ''  # ;)
        super_str += title_bar + '\n' + separator

        for row_index in range(len(self.ocean_fields)):
            super_str += side_bar_elements[row_index]
            for column_index in range(len(self.ocean_fields[row_index])):
                super_str += "|  {}  ".format(self.ocean_fields[row_index][column_index].__str__())
            super_str += '\n'
            super_str += separator

        return(super_str)
