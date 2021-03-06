from ocean import *
from player import *
from ship import *
from square import *
from main import *
from quiz import start
import os


class GameFlow():

    turn_count = 0
    difficulty_lvl = 1
    play_mode = ''

    def __init__(self):
        self.set_difficulty_lvl()
        self.player_one = self.choose_play_mode()
        self.player_two = Human(self.choose_players_name())

    def fight(self):

        while True:
            self.turn_count += 1
            self.player_one.perform_hit(self.player_two)
            if self.check_if_lose(self.player_two):
                self.player_one.display_game_message(self.player_two)
                print(self.player_two.board)
                return self.player_one
            self.player_two.perform_hit(self.player_one)
            if self.check_if_lose(self.player_one):
                self.player_two.display_game_message(self.player_one)
                print(self.player_one.board)
                return self.player_two

    def check_if_lose(self, player):

        total_hit_points = 0
        for ship in player.board.my_navy:
            total_hit_points += ship.hit_points
        if total_hit_points == 0:
            return True
        return False

    def choose_play_mode(self):
        play_modes = ['\n  1. Singleplayer', '  2. Multiplayer', '  3. Quiz\n']
        while True:
            self.print_list(play_modes)
            mode = input("  Choose game mode (pass the number): ")
            if mode == '1':
                self.play_mode = 1
                return AI(self.difficulty_lvl)
            elif mode == '2':
                self.play_mode = 2
                return Human(self.choose_players_name())
            elif mode == '3':
                start()
            else:
                print('Input must be a number from given scope.\n')

    def choose_players_name(self):
        name = ''
        while len(name) == 0 or len(name) > 15:
            name = input("\n  Choose players name(max 15 chars): ").strip()
        os.system('clear')
        return name

    @staticmethod
    def print_list(list):
        for element in list:
            print(element)

    def set_difficulty_lvl(self):
        levels = ['\n 1. Easy', ' 2. Medium', ' 3. Hard']
        self.print_list(levels)

        while True:
            difficulty_lvl = input("\n  Choose number of difficulty level: ").strip()
            if difficulty_lvl in ["1", "2", "3"]:
                break
            else:
                print("Input must be a number from given scope.\n")

        self.difficulty_lvl = int(difficulty_lvl)

    def init_hall_of_fame(self, round_count, winner_name, time):
        ''' Writes to hall_of_fame file.'''
        with open("HALL_OF_FAME.txt", "a", encoding='utf-8') as HALL_OF_FAME:
            user_stats = ['{:15.15}'.format(round_count),
                          '{:15.15}'.format(winner_name),
                          time]
            user_stats = "        ".join(user_stats)
            HALL_OF_FAME.write(str(user_stats) + "\n")
            print("Your stats has been saved!\n\n")

    def show_hall_of_fame(self):
        ''' Reads from and prints hall_of_fame file.'''
        with open("HALL_OF_FAME.txt", "r", encoding='utf-8') as HALL_OF_FAME:
            os.system("clear")
            print("\nHALL_OF_FAME:\n")
            print("ID     TURN COUNT             NAME                   TIME IN MINUTES\n\n")

            error_free_HALL_OF_FAME = []

            # It's best to check once per line if it will not return error while sorting,
            # to ensure a well - ordered & crash - free final list.
            for line in HALL_OF_FAME:
                try:
                    if int(line[0]):
                        error_free_HALL_OF_FAME.append(line)
                except ValueError:
                    pass

            list_place = 1
        for line in sorted(error_free_HALL_OF_FAME, key=lambda line: int(line.split()[0])):
            print('{:04d}'.format(list_place), ".", "".join(line))
            list_place += 1
