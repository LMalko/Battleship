from main import *
from player import *
from ship import *
from square import *
import sys


class Ocean():

    # fields = [[Square()*10]*10]

    def __init__(self, coordinants_dictionary):
        self.coordinants_dictionary = coordinants_dictionary
        self.fields = [[Square()*10]*10]    # 2 fory i append

    def set_ships_on_board(self, list):

        for ship in self.coordinants_dictionary.keys():     # dla klucza = nazwie klasy w str
            for coordinants in self.coordinants_dictionary.get(ship):   # wyciągnij wartość dla klucza(lista list ze współrzędnymi)
                del self.fields[coordinants[0]][coordinants[1]]     # wyczyść pozycję z pustego Square()

                self.fields[coordinants[0]].insert(coordinants[1], Square(getattr(sys.modules[__name__], ship)()))
                        # wstaw instancję Square zaimplementowaną konkretnym shipem 

'''
[[[1,2],[3,4], [5,6]]
[[1,2],[3,4], [5,6], [7,8]]]
'''
