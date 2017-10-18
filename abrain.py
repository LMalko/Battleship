"""This module contain AI mechanic."""

import random


class ABrain():
    """Abstract class with attribs and methods used in class AI(Player)."""
    # ai_memo (dict) contains coordinates of all past ai shots
    # key = coords, value = bool (True if shot was accurate)
    ai_memo = {}  # eg. {(0, 1): False}
    last_accurate_coords = ()
    # intelligence (integer) specify ai accuracy in shooting enemy ships
    # depends on game difficulty_lvl (GameFlow):
    #       easy: intelligence = 1
    #       normal: intelligence = 2
    #       hard: intelligence = 3
    intelligence = 1

    def search_and_try_destroy(self, opponent):
        tries_number = self.intelligence * 4
        if self.check_if_bother_last_accurate_coords(opponent):
            coords = self.check_coords_next_to(
                                                opponent,
                                                tries_number)
        else:
            coords = self.check_new_coords(opponent, tries_number)

        return coords

    def was_player_hit(self, x_coord, y_coord, opponent):
        """Check if opponent's ship was hit, returns bool."""
        condition_1 = opponent.board.fields[x_coord][y_coord].hit_count == 0
        condition_2 = opponent.board.fields[x_coord][y_coord].associated_class
        if condition_1 and condition_2:
            self.last_accurate_coords = (x_coord, y_coord)
            return True
        else:
            return False

    def check_new_coords(self, opponent, tries_number):
        coords = (10, 10)
        for tries in range(tries_number):
            x_coord = random.randint(0, 9)
            y_coord = random.randint(0, 9)
            checker = self.was_player_hit(x_coord, y_coord, opponent)
            coords = (x_coord, y_coord)
            if coords not in self.ai_memo:
                self.ai_memo[(coords)] = checker
            if checker:
                return coords
        return coords

    def check_coords_next_to(self, opponent, tries_number):
        for tries in range(tries_number):
            x_coord = self.last_accurate_coords[0]
            y_coord = self.last_accurate_coords[1]
            decide_if_horisontal = random.choice((True, False))
            if decide_if_horisontal:
                y_coord += random.choice((-1, 1))
            else:
                x_coord += random.choice((-1, 1))
            condition_1 = x_coord in range(0, 9)
            condition_2 = y_coord in range(0, 9)
            condition_3 = (x_coord, y_coord) not in self.ai_memo
            if condition_1 and condition_2 and condition_3:
                coords = (x_coord, y_coord)
                break
        checker = self.was_player_hit(x_coord, y_coord, opponent)
        coords = (x_coord, y_coord)
        if coords not in self.ai_memo:
            self.ai_memo[(coords)] = checker
        return coords

    def check_if_bother_last_accurate_coords(self, opponent):
        if self.last_accurate_coords:
            all_coords = list(self.ai_memo.keys())
            index = all_coords.index(self.last_accurate_coords)
            acceptable_topicality = 4
            for ship in opponent.board.my_navy:
                if ship.hit_points == 1:
                    acceptable_topicality = 6
                    break

            if index > len(all_coords) - acceptable_topicality:
                return True
        return False
