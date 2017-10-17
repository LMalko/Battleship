import os
from player import *
from ocean import *
from ship import *
from square import *


def main():
    os.system("clear")
    with open("battleship.md", "r", encoding="utf8") as myfile:
        myfile = myfile.read().splitlines() 
        for line in myfile:
            print(line)
    difficulty_level = input("Chosse difficulty: easy(1), medium(2), hard(3) --> ")
    this_game = GameFlow()
    this_game.set_difficulty_lvl(difficulty_level)


if __name__ == "__main__":
    main()
