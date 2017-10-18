from ship import *
from square import *
import sys


class Ocean():

    def __init__(self, coordinants_dictionary, fields):
        self.coordinants_dictionary = coordinants_dictionary
        self.fields = fields
        self.my_navy = []   # list of refs to players ship objects
        self.__set_ships_on_board()

    def __set_ships_on_board(self):

        for ship in self.coordinants_dictionary.keys():     # dla klucza = nazwie klasy w str
            ship_object = getattr(sys.modules[__name__], ship)()
            self.my_navy.append(ship_object)
            for list_of_coordinants in self.coordinants_dictionary.get(ship):   # lista w lista list ze współrzędnymi
                for coordinants in range(len(self.coordinants_dictionary.get(ship))):
                    x_coord = list_of_coordinants[0]    # współrzędna x
                    y_coord = list_of_coordinants[1]
                    self.fields[x_coord].pop(y_coord)    # wyczyść pozycję z pustego Square()
                    self.fields[x_coord].insert(y_coord, Square(ship_object))    # wstaw instancję Square zaimplementowaną konkretnym shipem 
       
    
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

        alfabet = "ABCDEFGHIJ"
        title_bar = ' |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  | 10 '
        separator = '-'*len(title_bar) + '\n'
        
        super_str = ''
        super_str += title_bar + '\n' + separator

        for lists in range(len(self.fields)):
            super_str += alfabet[lists]
            for element in range(len(self.fields[lists])):
                super_str += "|  {}  ".format(self.fields[lists][element].__str__())
            super_str += '\n'
            super_str += separator

        return(super_str)

# test_dict = {
#             'Battleship': [[2,3],[2,4],[2,5]],
#             'Cruiser': [[4,3],[4,2],[4,1]],
#             'Carrier': [[6,6],[7,6],[8,6]]}

# test_ocean = Ocean(test_dict)
# print(test_ocean)

