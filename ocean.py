from ship import *
from square import *
import sys


class Ocean():

    def __init__(self, coordinants_dictionary):
        self.coordinants_dictionary = coordinants_dictionary
        self.fields = []
        self.__fill_list_with_Square_obj()
        self.set_ships_on_board()


    def __fill_list_with_Square_obj(self):
        board_side_length = 10
        
        for empty_list in range(board_side_length):
            self.fields.append([])
            for single_element in range(board_side_length):
                self.fields[empty_list].append(Square())

    def set_ships_on_board(self):

        for ship in self.coordinants_dictionary.keys():     # dla klucza = nazwie klasy w str
            class_name = getattr(sys.modules[__name__], ship)()
            for list_of_coordinants in self.coordinants_dictionary.get(ship):   # lista w lista list ze współrzędnymi
                for coordinants in range(len(self.coordinants_dictionary.get(ship))):
                    x_coord = list_of_coordinants[0]    # współrzędna x
                    y_coord = list_of_coordinants[1]
                    self.fields[x_coord].pop(y_coord)    # wyczyść pozycję z pustego Square()
                    self.fields[x_coord].insert(y_coord, Square(class_name))    # wstaw instancję Square zaimplementowaną konkretnym shipem 
    def __str__(self):

        # ubot = Square(Submarine())        # kod do testów
        # ubot.was_hit()
        # self.fields[8][8] = ubot
        # print('hit count', self.fields[2][3].hit_count)
        # print('obj', self.fields[2][3].associated_class)
        # self.fields[2][3].was_hit()
        # print('hit count', self.fields[2][3].hit_count)
        # print('obj', self.fields[2][3].associated_class)
        # self.fields[2][3].was_hit()
        # print('hit count', self.fields[2][3].hit_count)
        # print('obj', self.fields[2][3].associated_class)
        # self.fields[2][3].was_hit()
        # print('hit count', self.fields[2][3].hit_count)
        # print('obj', self.fields[2][3].associated_class)

        super_str = ''
        for lists in range(len(self.fields)):
            for element in range(len(self.fields[lists])):
                super_str += " {}".format(self.fields[lists][element].__str__())
            super_str += '\n'

        return(super_str)

# test_dict = {
#             'Battleship': [[2,3],[2,4],[2,5]],
#             'Cruiser': [[4,3],[4,2],[4,1]],
#             'Carrier': [[6,6],[7,6],[8,6]]}

# test_ocean = Ocean(test_dict)
# print(test_ocean)

