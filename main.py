import os
import sys
import time
from game_flow import *


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
        #time.sleep(3)
        #os.system("clear")

    with open("battleship.md", "r", encoding="utf8") as myfile:
        myfile = myfile.read().splitlines() 
        for line in myfile:
            print(line)
    input("")
    os.system('clear')
    start_time = time.time()
    this_game = GameFlow()
    # print("---------->", Player.board)
    winner = this_game.fight()
    print("The winner is: ", winner.name)
    print("Zostałeś żeglarzem roku!")
    elapsed_time = (time.time() - start_time) / 60
    this_game.init_hall_of_fame(str(this_game.turn_count), winner.name, str(elapsed_time).split(".")[0])
    this_game.show_hall_of_fame()


if __name__ == "__main__":
    main()
