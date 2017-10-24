import random
from ocean import Ocean
from ship import Destroyer, Submarine, Cruiser, Battleship, Carrier
from square import Square
from abrain import ABrain
from ship_position_picker import get_ship_dictionary_from_user_input
import os
import sys
import ship_generator


class Player():
    # Containts Player's created ships.
    my_ships = {}
    # Length of title bar of players ocean-board.
    board_row_len = 0
    # Empty message box, will be filled druing game.
    game_message = [' ', ' ', ' ', ' ', ' ']

    def perform_hit(self, opponent):
        """ Executes attack to chosen quater in opponent board. """
        os.system('clear')
        self.display_game_message(opponent)
        if isinstance(self, Human):
            print(opponent.board)
            print('\n')
            print(self.board)
        coordinants = self.choose_attack_coordinates(opponent)
        x_coord_index = 0
        y_coord_index = 1
        x_coord = coordinants[x_coord_index]
        y_coord = coordinants[y_coord_index]

        # Delate the oldest message in message box.
        del self.game_message[0]
        # Add new message to the message box.
        self.game_message.append(self.name + ' ' + opponent.board.ocean_fields[x_coord][y_coord].was_hit())

    def display_game_message(self, opponent):
        """
        Concatenates two lists rows into one string and prints it as a table.
        Display box with game meggages (first list) and players ship inventory (second list)

        opponent: another Player object
        """
        separator = '-'*self.board_row_len
        half_separator = '-'*int(self.board_row_len/2)
        message_box = []
        # Return formatted string with players ship inventory.
        players_navy = self.__str__().split('\n')
        separator_index = 0

        message_box.append(separator)
        for message in self.game_message:
            message_box.append(" | Gameplay: {}".format(message).ljust(self.board_row_len))
        message_box.append(half_separator.ljust(self.board_row_len))
        message_box.append(" | Game info: {} toure:".format(self.name).ljust(self.board_row_len))
        message_box.append(separator)

        for index in range(len(message_box)):
            print(message_box[index], players_navy[index])

    def get_ships_placement(self):
        """ Returns dict with ship coordinates. """
        self.my_ships = self._initialize_ship_coordinates()

    def _initialize_ocean_fields(self):
        board_side_length = 10
        self.ocean_fields = []
        for height in range(board_side_length):
            row = []
            for width in range(board_side_length):
                row.append(Square())
            self.ocean_fields.append(row)

    def __str__(self):
        navy_str = ''

        title_bar = ' | ' + self.name + ' navy:'
        separator = '-'*int(len(title_bar)) + '\n'

        for ship in self.board.my_navy:
            formatted_str = " | {}".format(ship)
            navy_str += formatted_str + '\n'
            separator_len = int(len(formatted_str))

        separator = '-' * separator_len + '\n'

        return separator + title_bar.ljust(separator_len) + '\n' + separator + navy_str + separator


class Human(Player):
    """This is User-Player class."""

    def __init__(self, name):
        self.name = name
        # Gets ship.
        self.get_ships_placement()
        self._initialize_ocean_fields()
        # Create players board.
        self.board = Ocean(self.my_ships, self.ocean_fields)
        board_bar_len = self.board.__str__().split('\n')
        # Ustawia długość belki do printów.
        Player.board_row_len = len(board_bar_len[0])

    def choose_attack_coordinates(self, opponent):
        """ Returns coordinates in list [x, y]."""
        print('   ' + self.name + ", it's bombard time! \n   Please specify attack coordinates:\n")
        return self._input_and_check_coordinates()

    def _initialize_ship_coordinates(self):
        """ Returns dict of ships placement coordinates. """
        return get_ship_dictionary_from_user_input()

    def _input_and_check_coordinates(self):
        """ Returns list of coordinates. """
        correct_letters = "ABCDEFGHIJ"
        invalid_input_info = "invalid input."
        coordinate = []
        row_index = ""
        while not row_index or row_index not in correct_letters:
            row_index = input("      Please, specify row (A - J): ").upper()
            # Goes one line up.
            sys.stdout.write("\033[F")
            # Clears the line.
            sys.stdout.write("\033[K")
        coordinate.append(correct_letters.index(row_index))
        while True:
            try:
                column_index = int(input("      Please, specify column (1 - 10): "))
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                if column_index in range(1, 11):
                    coordinate.append(column_index - 1)
                    break

            except ValueError:
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        return coordinate


class AI(Player, ABrain):
    """This is AI-Player class."""

    name = "AI"

    def __init__(self, iq):
        self.ocean_fields = []
        self._initialize_ocean_fields()
        self.get_ships_placement()
        # Create board.
        self.board = Ocean(self.my_ships, self.ocean_fields)
        self.intelligence = iq

    def _initialize_ship_coordinates(self):
        """ AI generate ships placement (coordinates). Returns dict of ships placement coordinates. """
        return ship_generator.generate_ship_coords(self.ocean_fields)

    def choose_attack_coordinates(self, opponent):
        """ Choose attack (coordinates) by AI. Returns coordinates in list [x, y]."""
        return self.search_and_try_destroy(opponent)


# ####### USTAW:
poziom_trudnosci = 3  # 1 lub 2 lub 3
ilosc_szybkich_tur = 65  # lepiej nie więcej niż 70

comp = AI(poziom_trudnosci)
mentor = Human("Mentor")
comp.perform_hit(opponent=mentor)
turn = 0
for i in range(ilosc_szybkich_tur):
    comp.perform_hit(opponent=mentor)
    print("main last_accurate_coords", comp.last_accurate_coords)
    print(mentor.board)
    print('ostatnie skuteczne:', comp.last_accurate_coords)
    print('moja pamięć', comp.ai_memo)
    print('ilość zapamiętanych:', len(comp.ai_memo))
    print('tura:', turn)
    pause = input()
    turn += 1
# print(comp.last_accurate_coords, comp.ai_memo)

# print(jarek.board)
