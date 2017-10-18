import os
import time
from game_flow import *


def delay_print(s):
    """ Delays printing. """
    for c in s:
        sys.stdout.write("%s" % c)
        sys.stdout.flush()
        time.sleep(0.010)


def main():

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

    this_game = GameFlow()
    winner = this_game.fight()
    print("The winner is: ", winner.name)
    print("Zostałeś żeglarzem roku!")


if __name__ == "__main__":
    main()
