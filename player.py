
import random
from ocean import Ocean
from ship import Destroyer, Submarine, Cruiser, Battleship, Carrier
from square import Square
from abrain import ABrain  # new AI abstract class
from ship_position_picker import get_ship_dictionary_from_user_input
import os
# import time
import sys
import ship_generator


class Player():
    """Abstract Player class."""
    name = "Noname" #po cooooooo to tu?
    # Player's availible ships:
    ships = [Destroyer, Submarine] #, Cruiser, Battleship, Carrier]
    my_ships = {}  # containts Player's created ships
    board_row_len = None  # Ocean object
    game_message = [' ', ' ', ' ', ' ']

    def perform_hit(self, opponent):
        """
        Execute attack to chosen quater in opponent board.

        opponent: another Player object
        coordinates: list [x, y] (x, y: integers)
        """
        os.system('clear')

        self.display_message(opponent)

        if isinstance(self, Human):
            print(opponent.board)
            print(self)
        # if isinstance(self, AI):
        #     input("PRESS ANY KEY TO CONTINUE".center(self.board_row_len))
        coords = self.choose_attack_coordinates(opponent)
        x_coord = coords[0]
        y_coord = coords[1]

        del self.game_message[0]
        self.game_message.append(self.name + ' ' + opponent.board.fields[x_coord][y_coord].was_hit())   #gdyby zt tutuaj miss/hit/sunk możnaby printować info message z nazwą playera itp
        # if isinstance(self, Human):

        
    def display_message(self, opponent):
        separator = '-'*self.board_row_len

        print(separator)
        for message in self.game_message:
            print(" | Game info: {}".format(message))
        print(separator[:int(len(separator)/2)])           
        print(" | Game info: {} toure:".format(self.name))    
        print(separator)

    def get_ships_placement(self):
        """
        Choose ships placement (coordinates) by Player.

        Returns dict with ship coordinates, eg.
        {"Destroyer": [[0, 0], [0, 1], "Submarine": ...}
        """
        self.my_ships = self._set_coordinates()

    def fill_list_with_Square_obj(self):
        board_side_length = 10

        for empty_list in range(board_side_length):
            self.fields.append([])
            for single_element in range(board_side_length):
                self.fields[empty_list].append(Square())

class Human(Player):
    """This is User-Player class."""

    def __init__(self, name):
        self.name = name
        self.get_ships_placement()
        self.fields = []
        self.fill_list_with_Square_obj()
        self.board = Ocean(self.my_ships, self.fields)  # create board
        board_bar_len = self.board.__str__().split('\n')
        Player.board_row_len = len(board_bar_len[0]) # ustawia długość belki do printów

    def choose_attack_coordinates(self, opponent):
        """
        Choose attack (coordinates) by Player.

        Returns coordinates in list [x, y]
        """
        print('   ' + self.name + ", it's bombard time! \n   Please specify attack coordinates:\n")
        return self._input_and_check_coordinates()

    def _set_coordinates(self):
        """
        Input coordinates by User (format: A1, B1, etc..).

        Check if input is correct.
        Transform Player's coordinates to right indexing form.
        Get inputed x, y coordinates (format: [A, 1], [A, 2]).
        Tranform to format [0, 0] to use for correct indexing.

        Returns dict of ships placement coordinates.
        """
        return get_ship_dictionary_from_user_input()
        
    def _input_and_check_coordinates(self):
        """
        Take coordinates from Player.

        Check if input is correct.
        Transform Player's coordinates to right indexing form.
        Get inputed x, y coordinates (format: [A, 1], [A, 2]).
        Tranform to format [0, 0] to use for correct indexing.

        Returns list of coordinates, eg. [5, 1]
        """
        correct_letters = "ABCDEFGHIJ"
        invalid_input_info = "invalid input."
        coordinate = []
        row_index = ""
        while not row_index or row_index not in correct_letters:
            row_index = input("      Please, specify row (A - J): ").upper()
            sys.stdout.write("\033[F")  # goes one line up
            sys.stdout.write("\033[K")  # clears the line
        coordinate.append(correct_letters.index(row_index))
        while True:
            try:
                column_index = int(input("      Please, specify column (1 - 10): "))
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                if column_index in range(1, 11):
                    coordinate.append(column_index - 1)
                    break
                else:
                    print(invalid_input_info)

            except:
                print(invalid_input_info)
        return coordinate


    @staticmethod
    def choose_ship_picture(ship_instance):
        filenames = ["cruiser_PHOTO.md", "battleship_PHOTO.md",
                     "carrier_PHOTO.md", "submarine_PHOTO.md", "destroyer_PHOTO.md"]
        if ship_instance.__name__ == "Cruiser":
            Human.print_ship_picture("cruiser_PHOTO.md")
        elif ship_instance.__name__ == "Battleship":
            Human.print_ship_picture("battleship_PHOTO.md")
        elif ship_instance.__name__ == "Carrier":
            Human.print_ship_picture("carrier_PHOTO.md")
        elif ship_instance.__name__ == "Submarine":
            Human.print_ship_picture("submarine_PHOTO.md")
        elif ship_instance.__name__ == "Destroyer":
            Human.print_ship_picture("destroyer_PHOTO.md")

    @staticmethod
    def print_ship_picture(filename):               ###################tego już nie będziemy używać
        with open(filename, "r", encoding="utf8") as myfile:
            myfile = myfile.read().splitlines()
            for line in myfile:
                print(line)

    def __str__(self):

        navy_str = ''
        tab_title = '   ' + self.name + ' navy:\n'
        separator = '-'*int(len(tab_title)) + '\n'

        navy_str +=  separator + tab_title + separator
        for ship in self.board.my_navy:
            navy_str += " - {}\n".format(ship)

        return navy_str + separator

class AI(Player, ABrain):
    """This is AI-Player class."""

    name = "AI"

    def __init__(self):
        self.fields = []
        self.fill_list_with_Square_obj()
        self.get_ships_placement()
        self.board = Ocean(self.my_ships, self.fields)  # create board

    def _set_coordinates(self):
        """
        AI generate ships placement (coordinates).

        Returns dict of ships placement coordinates.
        """
        # # tutaj metoda Michała
        # # # tymczasowo:
        # test_dict = {
        #             'Battleship': [[2, 3], [2, 4], [2, 5], [2, 6]]} #,
        #             # 'Cruiser': [[4,3],[4,2],[4,1]],
        #             # 'Carrier': [[6,6],[7,6],[8,6]]
        #             # }
        # return test_dict  # temporary
        return ship_generator.generate_ship_coords(self.fields)

    def choose_attack_coordinates(self, opponent):
        """
        Choose attack (coordinates) by AI.

        Returns coordinates in list [x, y].
        """
        return self.search_and_try_destroy(opponent)

    def __str__(self):
        board = self.board.__str__()
        board_lines = board.split('\n')
        separator = board_lines[1] + '\n'

        navy_str = separator
        navy_str += '   ' + self.name + ' navy:\n' + separator
        for ship in self.board.my_navy:
            navy_str += " | {}\n".format(ship)

        return navy_str + separator
#
comp = AI()
# jarek = Human("Jarek")
# print(comp.board)
# print(jarek.board)
# comp.perform_hit(opponent=jarek)
# jarek.perform_hit(opponent=comp)
# print(isinstance(comp, Human))
