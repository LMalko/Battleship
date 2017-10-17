# from main import *
from ocean import *
from player import *
from ship import *
from square import *


class GameFlow():

    turn_count = 0
    difficulty_lvl = 0

    def __init__(self):

        self.player_one = self.choose_play_mode()
        self.player_two = Human()

    @staticmethod
    def choose_play_mode():
        play_modes = ['Choose game mode:', ' 1. Singleplayer', ' 2. Multiplayer']
        while True:
            for line in play_modes:
                print(line)
            mode = input(" Pass mode number: ")
            if mode == '1':
                return AI()
            elif mode == '2':
                return Human()
            else:
                print('Input must be a number from given scope.\n')        


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


# test_gameflow = GameFlow()
# print('AAAAAAA')
# test_gameflow.choose_play_mode()
