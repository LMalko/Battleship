import time
import os


def summary(correct_answers_count):
    '''Print correct/ all answers ratio.'''

    os.system("clear")
    print("\n\n\nYour result is: " + str(correct_answers_count) + " out of 7")
    time.sleep(3)
    os.system("clear")


def quiz_flow(questions, answers):

    question_number = answers_set_number = correct_answer_index_number = correct_answers_count = 0
    correct_answer_index_numbers_list = [3, 2, 0, 2, 0, 1, 2]

    for e in questions:
        print(e)
        for i in answers[answers_set_number]:
            print(i)
        while True:
            try:
                user_answer = int(input("Your choice is (choose 1, 2, 3 or 4): "))
            except ValueError:
                print("Please put number")
                continue
            if user_answer not in [1, 2, 3, 4]:
                print("No such answer, try again")
                continue
            index_numerical_difference = 1
            user_answer -= index_numerical_difference
            break
        if user_answer == correct_answer_index_numbers_list[correct_answer_index_number]:
            os.system("clear")
            print("Correct!!!")
            time.sleep(2)
            os.system("clear")
            correct_answers_count += 1
        else:
            os.system("clear")
            print("No.\nCorrect answer is ",
                  answers[question_number]
                  [(correct_answer_index_numbers_list[correct_answer_index_number])])
            time.sleep(2)
            os.system("clear")

        question_number += 1
        answers_set_number += 1
        correct_answer_index_number += 1

    summary(correct_answers_count)


def main():
    os.system("clear")
    print("WELCOME TO BATTLESHIP QUIZ - najnudniejszym quizie w sieci !!\nAnswer the following questions:\n\n")

    questions = ["Back part of a ship is: \n", "Middle part of a ship is: \n",
                 "Area used for carrying goods is: \n", "Bed on a ship is: \n",
                 "Place from which a ship is controlled: \n",
                 "Place where prisoners are kept: \n", "Private room on a ship: \n"]

    answers = [["Cabin", "Helm", "Galley", "Stern", "\n"],
               ["Deck", "Wardroom", "Amidships", "Sickbay", "\n"],
               ["Bay", "Helm", "Tiller", "Porthole"],
               ["Mainsail", "Wardroom", "Berth", "Rigging"],
               ["Bridge", "Mast", "Port", "Helm"],
               ["Cabin", "Brig", "Gangway", "Sickbay"],
               ["Crow's Nest", "DUPA_JEŻA", "Cabin", "Stern"]]

    quiz_flow(questions, answers)


if __name__ == "__main__":

    main()
