"""This module contain AI mechanic."""

import random


class ABrain():
    """Abstract class with attribs and methods used in class AI(Player)."""
    # ai_memo (dict) contains coordinates of all past ai shots
    # key = coords, value = bool (True if shot was accurate)
    ai_memo = {}  # {(11, 11): False}  # eg. {(0, 1): False}
    # intelligence (integer) specify ai accuracy in shooting enemy ships
    # depends on game difficulty_lvl (GameFlow):
    #       easy: intelligence = 1
    #       normal: intelligence = 2
    #       hard: intelligence = 3
    intelligence = 1

    def search_and_try_destroy(self, opponent):
        # _tmp_list = [self.ai_memo.keys()]
        # if _tmp_list[-1]:
        #     print(_tmp_list[-1])
        for tries in range(self.intelligence):
            x_coord, y_coord = 10, 10
            while (x_coord, y_coord) not in self.ai_memo.keys():
                x_coord = random.randint(0, 9)
                y_coord = random.randint(0, 9)
                # print("jestem w s&d:", x_coord, y_coord)
                checker = self.was_player_hit(x_coord, y_coord, opponent)
                self.ai_memo[(x_coord, y_coord)] = checker
                # print(self.ai_memo)
            # if checker:
            #     print(checker)
            #     print([x_coord, y_coord])
        return [x_coord, y_coord]

    def was_player_hit(self, x_coord, y_coord, opponent):
        """Check if opponent's ship was hit, returns bool."""
        condition_1 = opponent.board.fields[x_coord][y_coord].hit_count == 0
        condition_2 = opponent.board.fields[x_coord][y_coord].associated_class
        if condition_1 and condition_2:
            return True
        else:
            return False
