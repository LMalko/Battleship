
import random
from main import *
from ocean import Ocean
from ship import Destroyer, Submarine, Cruiser, Battleship, Carrier
from square import Square
from game_flow import GameFlow


class Player(GameFlow):
    """Abstract Player class."""
    name = "Noname"
    # Player's availible ships:
    ships = [Destroyer, Submarine, Cruiser, Battleship, Carrier]
    my_ships = {}  # containts Player's created ships
    board = None  # Ocean object

    def perform_hit(self, opponent, coordinates):
        """
        Execute attack to chosen quater in opponent board.

        opponent: another Player object
        coordinates: list [x, y] (x, y: integers)
        """
        # x = coordinates[0]
        # y = coordinates[1]
        # opponent.board[x][y]
        return coordinates  # może to wystarczy?

    def choose_ships_placement(self):
        """
        Choose ships placement (coordinates) by Player.

        Returns dict with ship coordinates, eg.
        {"Destroyer": [[0, 0], [0, 1], "Submarine": ...}
        """
        return self._set_coordinates()


class Human(Player):
    """This is User-Player class."""

    def __init__(self, name):
        self.name = name
        coordinates = self.choose_ships_placement()
        print(coordinates)
        print(type(coordinates))
        self.board = Ocean(coordinates)  # create board

    def choose_attack_coordinates(self):
        """
        Choose attack (coordinates) by Player.

        Returns coordinates in list [x, y]
        """
        print("It's bombard time, please specify attack coordinates:\n")
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
        all_ships_coordinates = {}
        type_letter = "Please, specify X (choose letter between A - J): "
        correct_letters = "ABCDEFGHIJ"
        type_number = "Please, specify Y (choose number between 1 - 10): "
        invalid_input_info = "invalid input."
        for ship in self.ships:
            Human.choose_ship_picture(ship)
            ship_coordinates = []
            for element in range(ship.hit_points):
                coordinate = self._input_and_check_coordinates()
                ship_coordinates.append(coordinate)
                print(ship_coordinates)  # tmp
            # BĘDZIE ZUPEŁNIE INACZEJ
            # metoda Michała - walidacja
            all_ships_coordinates[ship.__name__] = ship_coordinates
            print(all_ships_coordinates)  # temporary

        return all_ships_coordinates

    def _input_and_check_coordinates(self):
        """
        Take coordinates from Player.

        Check if input is correct.
        Transform Player's coordinates to right indexing form.
        Get inputed x, y coordinates (format: [A, 1], [A, 2]).
        Tranform to format [0, 0] to use for correct indexing.

        Returns list of coordinates, eg. [5, 1]
        """
        type_letter = "Please, specify X (choose letter between A - J): "
        correct_letters = "ABCDEFGHIJ"
        type_number = "Please, specify Y (choose number between 1 - 10): "
        invalid_input_info = "invalid input."
        coordinate = []
        row_index = ""
        while not row_index or row_index not in correct_letters:
            row_index = input(type_letter).upper()
        coordinate.append(correct_letters.index(row_index))
        while True:
            try:
                column_index = int(input(type_number))
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
    def print_ship_picture(filename):
        with open(filename, "r", encoding="utf8") as myfile:
            myfile = myfile.read().splitlines()
            for line in myfile:
                print(line)


class AI(Player):
    """This is AI-Player class."""

    name = "AI"
    intelligence = 1  # determines effectiveness of bombard

    def __init__(self):
        coordinates = self.choose_ships_placement()
        self.board = Ocean(coordinates)  # create board

    def _set_coordinates(self):
        """
        AI generate ships placement (coordinates).

        Returns dict of ships placement coordinates.
        """
        # tutaj metoda Michała
        # tymczasowo:
        test_dict = {
                    'Battleship': [[2,3],[2,4],[2,5]],
                    'Cruiser': [[4,3],[4,2],[4,1]],
                    'Carrier': [[6,6],[7,6],[8,6]]}
        return test_dict  # temporary

    def choose_attack_coordinates(self):
        """
        Choose attack (coordinates) by AI.

        Returns coordinates in list [x, y].
        """
        # tymczasowo w prymitywnej formie (ok dla easy mode):
        if self.intelligence == 1:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
        return [x, y]


# jarek = Human("Jarek")
# comp = AI()
# print(jarek.choose_attack_coordinates())
# print(comp.choose_attack_coordinates())
# print(jarek.board)
