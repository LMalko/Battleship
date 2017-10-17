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
    while True:
        difficulty_level = input("Chosse difficulty: easy(1), medium(2), hard(3) -->")
        if difficulty_level not in ["1", "2", "3"]:
            print("Please choose from 1, 2 or 3")
            continue
        else:
            break
    this_game = GameFlow()
    this_game.set_difficulty_lvl(difficulty_level)


if __name__ == "__main__":
    main()
