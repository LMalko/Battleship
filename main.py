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




"""
def hall_of_fame(hero, start_time):
    """ Exports to and reads from hall of fame.txt."""
    os.system("clear")
    finish_time = datetime.datetime.now()
    # Get rid of microseconds.
    game_time = (str(finish_time - start_time)).split(".")[0]
    # Sum up attributes.
    sum_of_attributes = 0
    for value in hero.attrib_dict.values():
        try:
            sum_of_attributes += int(value)
        except ValueError:
            continue
    user_name = input("\nWpisz swoje prawdziwe imię: ")
    print("\nGratulacje,", user_name, ".Twoje osiągnięcia zostaną zapisane.\n")
    print("ATRYBUTY NA KONIEC: \n")
    # User_name length must = 20.
    user_name = '{:.20}'.format(user_name)
    user_name += " " * (20 - len(user_name))
    for k, v in hero.attrib_dict.items():
        print(k, ":", v)
    print("\nCZAS GRY: ", game_time, "\nSUMA ATRYBUTÓW: ", sum_of_attributes,
          "\nKLASA: ", hero.proffession)
    # Add final results to Hall of Fame.
    with open("HALL_OF_FAME.txt", "a", encoding='utf-8') as HALL_OF_FAME:
        user_score = [str(sum_of_attributes), str(user_name), str(game_time),
                      str(hero.proffession)]
        user_score = "        ".join(user_score)
        HALL_OF_FAME.write(str(user_score) + "\n")
        print("\x1b[6;31;47m" + "Wciśnij cokolwiek." + "\x1b[0m")
        input_char = getch()
    with open("HALL_OF_FAME.txt", "r", encoding='utf-8') as HALL_OF_FAME:
        os.system("clear")
        print("\nHALL_OF_FAME:\n")
        # Use pre-calculated number of spaces to fit the results.
        print(" " * 3,  "PUNKTY", " " * 2, "GRACZ", " " * 21, "CZAS", " " * 9, "KLASA\n")
        HALL_OF_FAME = sorted(HALL_OF_FAME.readlines(), reverse=True)
        list_place = 1
        for i in HALL_OF_FAME:
            # Format list place display to {:04d}.
            print('{:04d}'.format(list_place), ".", "".join(i))
            list_place += 1
        print("\x1b[6;31;47m" + "Wciśnij 'Y' żeby zagrać jeszcze raz, coś innego żeby wyjść." + "\x1b[0m")
        input_char = getch()
        os.system("clear")
        if input_char.upper() == "Y":
            main()
        else:
sys.exit()
"""