import os
import sys
import time
from game_flow import *
from ship_position_picker import getch_single_character


def delay_print(s):
    """ Delays printing. """
    for c in s:
        sys.stdout.write("%s" % c)
        sys.stdout.flush()
        time.sleep(0.010)


def main():
    sys.stdout.write("\x1b[8;100;200t")     # sets terminal width to 100 x 200
    os.system("clear")

    #with open("story.md", "r", encoding="utf8") as myfile:
        #for line in myfile:
            #delay_print(line)
        #getch_single_character()
        #os.system("clear")

    with open("battleship.md", "r", encoding="utf8") as myfile:
        myfile = myfile.read().splitlines() 
        for line in myfile:
            print(line)
    getch_single_character()
    os.system('clear')
    start_time = time.time()
    this_game = GameFlow()
    # print("---------->", Player.board)
    winner = this_game.fight()
    print("The winner is: ", winner.name)
    elapsed_time = str((time.time() - start_time) / 60).split(".")[0]
    if winner.name == "AI":
        print("Computer wins, You die.")
    else:
        print("\n\nZostałeś żeglarzem roku!")
        print("Your result,", winner.name, "is:", this_game.turn_count, "turns in", elapsed_time, "minutes.")
    this_game.init_hall_of_fame(str(this_game.turn_count), winner.name, elapsed_time)
    print("Press enter to continue.")
    getch_single_character()
    this_game.show_hall_of_fame()


if __name__ == "__main__":
    main()
