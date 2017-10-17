from main import *
from ocean import *
from player import *
from ship import *
from square import *


class GameFlow():

    turn_count = 0
    difficulty_lvl = 0
    player_one = None
    player_two = None

    def __init__(self):

        self.player_one = Player()
        self.player_two = Player()

    def set_difficulty_lvl(self, difficulty_lvl):
        while True:
            if difficulty_lvl not in ["1", "2", "3"]:
                print("Please choose from 1, 2, 3")
                continue
            else:
                break

        self.difficulty_lvl = difficulty_lvl

    def init_hall_of_fame(self, filename):
        with open(filename, "a", encoding="utf8") as myfile:
            myfile.write(self.COŚTAM)               # wpisać co wysyłamy do pliku(self.name + self.turn_count ?)

    def show_hall_of_fame(self, filename):
        with open(filename, "r", encoding="utf8") as myfile:
            for line in myfile:
                print(line)
