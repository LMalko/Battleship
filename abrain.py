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
    should_search_horisontal = False
    should_search_vertical = False

    def search_and_try_destroy(self, opponent):
        if self.check_if_bother_last_accurate_coords(opponent):
            coords = self.check_coords_next_to(opponent)
        else:
            coords = self.check_new_coords(opponent)
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

    def check_new_coords(self, opponent):
        difficulty_modifier = 2
        tries_number = self.intelligence * difficulty_modifier
        coords = (10, 10)  # starting tmp coords
        for tries in range(tries_number):
            for check in range(20):
                x_coord = random.randint(0, 9)
                y_coord = random.randint(0, 9)
                if self.check_if_new_coords_in_board_and_not_in_memo(
                                                                    x_coord,
                                                                    y_coord):
                    break
            checker = self.was_player_hit(x_coord, y_coord, opponent)
            coords = (x_coord, y_coord)
            self.remember_used_coords(coords, checker)
            if checker:
                return coords
        return coords

    def check_coords_next_to(self, opponent):
        x_coord = self.last_accurate_coords[0]
        y_coord = self.last_accurate_coords[1]
        if self.should_search_vertical or self.should_search_horisontal:
            if self.should_search_vertical and self.intelligence != 1:
                coords = self.search_horison_or_vert(
                                                    x_coord, y_coord,
                                                    opponent,
                                                    mode="vertical")
            else:
                coords = self.search_horison_or_vert(
                                                    x_coord, y_coord,
                                                    opponent,
                                                    mode="horisontal")
        else:
            decide_if_horisontal = random.choice((True, False))
            if decide_if_horisontal:
                coords = self.search_horison_or_vert(
                                                    x_coord, y_coord,
                                                    opponent,
                                                    mode="horisontal")
            else:
                coords = self.search_horison_or_vert(
                                                    x_coord, y_coord,
                                                    opponent,
                                                    mode="vertical")
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

    def remember_used_coords(self, coords, checker):
        if coords not in self.ai_memo:
            self.ai_memo[(coords)] = checker

    def check_if_new_coords_in_board_and_not_in_memo(self, x_coord, y_coord):
        condition_1 = x_coord in range(0, 9)
        condition_2 = y_coord in range(0, 9)
        condition_3 = (x_coord, y_coord) not in self.ai_memo
        if condition_1 and condition_2 and condition_3:
            return True
        return False

    def search_horison_or_vert(
                                self, x_coord, y_coord,
                                opponent, mode="horisontal"):
        if mode == "horisontal":
            coord = y_coord
        else:
            coord = x_coord
        for num in (-1, 2):
            coord += num
            if mode == "horisontal":
                y_coord = coord
            else:
                x_coord = coord
            if self.check_if_new_coords_in_board_and_not_in_memo(
                                                            x_coord,
                                                            y_coord):
                checker = self.was_player_hit(
                                                x_coord,
                                                y_coord, opponent)
                coords = (x_coord, y_coord)
                self.remember_used_coords(coords, checker)
                if checker:
                    if mode == "horisontal":
                        self.should_search_horisontal = True
                    else:
                        self.should_search_vertical = True
                return coords
        else:
            if mode == "horisontal":
                self.should_search_horisontal = False
            else:
                self.should_search_vertical = False
            coords = self.check_new_coords(opponent)
            return coords
