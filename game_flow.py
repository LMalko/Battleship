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
        self.player_two = Human(self.choose_players_name())

    def fight(self):
        # wywołane z maina, pętla  zt zwycięzcę(Playera) (?)
        # z maina można go wpisać do hall of fame itp
        # zaczyna wybrany czy losowy gracz?
        while True:
            self.turn_count += 1
            self.player_one.perform_hit(self.player_two) # brak drugiego arg - coordinants powinien pobierać już w perform_hit()
            if self.check_if_lose(self.player_two):
                return self.player_one
            self.player_two.perform_hit(self.player_one)    # -||-
            if self.check_if_lose(self.player_one):
                return self.player_two


    def check_if_lose(self, player):    #obj klasy Player (któryś z graczy)
        # spr sumę punktów życia posiadanych statków. Jeśli == 0 to przegrał
        # w Ocean można zrobić dodatkową liste przechowującą referencję do każdego statku umieszczonego na boardzie
        # w ten sposób łatwiej będzie tu sumować W PĘTLI ich punkty życia:
        #  total_hit_points = 0
        #  for ship in player.board.MOJA_FLOTA:
        #      total_hit_points += ship.hit_points
        #  if total_hit_points == 0:
        #       return True
        #  return False
        pass
        

    def choose_play_mode(self):
        play_modes = ['Choose game mode:', ' 1. Singleplayer', ' 2. Multiplayer']
        while True:
            for line in play_modes:
                print(line)
            mode = input(" Pass mode number: ")
            if mode == '1':
                return AI()
            elif mode == '2':
                return Human(self.choose_players_name())
            else:
                print('Input must be a number from given scope.\n')        

    def choose_players_name(self):
        name = ''
        while len(name) == 0:
            name = input("Choose players name: ").strip()

        return name

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
            myfile.write(self.DO_USTALENIA)               # wpisać co wysyłamy do pliku(self.name + self.turn_count ?)

    def show_hall_of_fame(self, filename):
        with open(filename, "r", encoding="utf8") as myfile:
            for line in myfile:
                print(line)


test_gameflow = GameFlow()
print('AAAAAAA')
for ship in test_gameflow.player_two.board.my_navy:
    print(ship)
# test_gameflow.choose_play_mode()    # niepotrzebne, bo powołując instancje wykonuje się init w którym to już jest
