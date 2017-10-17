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


if __name__ == "__main__":
    main()
