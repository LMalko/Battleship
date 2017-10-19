"""This module contain AI mechanic."""

import random


class ABrain():
    """Abstract class with attribs and methods used in class AI(Player)."""
    # ai_memo (dict) contains coordinates of all past ai shots:
    #   key = coords, value = bool (True if shot was accurate)
    ai_memo = {}  # eg. {(0, 1): False}
    last_accurate_coords = ()
    # intelligence (integer) specify ai accuracy in shooting enemy ships
    # depends on game difficulty_lvl (GameFlow):
    #       easy: intelligence = 1
    #       normal: intelligence = 2
    #       hard: intelligence = 3
    intelligence = 1
    # should_search_... is part of ai memory,
    # which has influence on ai choices:
    should_search_horisontal = False
    should_search_vertical = False

    def search_and_try_destroy(self, opponent):
        """Start searching & shooting process, returns coordinates."""
        # if the last accurate shot was not long ago:
        if self.check_if_bother_last_accurate_coords(opponent):
            # try in fields in neighborhood:
            coords = self.check_coords_next_to(opponent)
        else:
            # or try in new fields
            coords = self.check_new_coords(opponent)
        return coords

    def was_player_hit(self, x_coord, y_coord, opponent):
        """Check if opponent's ship was hit, returns bool."""
        condition_1 = opponent.board.fields[x_coord][y_coord].single_square_hit_count == 0
        condition_2 = opponent.board.fields[x_coord][y_coord].associated_class
        if condition_1 and condition_2:
            self.last_accurate_coords = (x_coord, y_coord)
            return True
        else:
            return False

    def check_new_coords(self, opponent):
        """
        Check (random choice) new attack coordinates.
        tries_number: (integer) specify number of tries, formula:
            AI's intelligence * difficulty_modifier
        tries_modifier: (integer) higher means more tries for AI.
        Returns attack coordinates.
        """
        tries_modifier = 1
        tries_number = self.intelligence * tries_modifier
        coords = (10, 10)  # starting tmp coords
        for tries in range(tries_number):
            for check in range(40):
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
        # if can't find any unused field to attack:
        if coords == (10, 10):
            coords = self.find_field_in_desperado_mode(opponent)
            return coords
        else:
            return coords

    def check_coords_next_to(self, opponent):
        """Check fields in neighborhood of last accurate shot."""
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
        """
        Check if it makes sense to relate to last accurate shot.
        acceptable_topicality: (integer) increases the tolerance
            for the use of past results.
        Returns bool.
        """
        if self.last_accurate_coords:
            all_coords = list(self.ai_memo.keys())
            index = all_coords.index(self.last_accurate_coords)
            acceptable_topicality = 3
            for ship in opponent.board.my_navy:
                if ship.hit_points == 1:
                    acceptable_topicality = 6
                    break

            if index > len(all_coords) - acceptable_topicality:
                return True
        return False

    def remember_used_coords(self, coords, checker):
        """Save result of last shot in memory."""
        if coords not in self.ai_memo:
            self.ai_memo[(coords)] = checker

    def check_if_new_coords_in_board_and_not_in_memo(self, x_coord, y_coord):
        """
        Take coordinates and check if they're not in memory (so they're fresh).
        Check if coordinates are in correct range (0, 9).
        Reason: AI can save them as new result.
        Returns bool.
        """
        condition_1 = x_coord in range(0, 9)
        condition_2 = y_coord in range(0, 9)
        condition_3 = (x_coord, y_coord) not in self.ai_memo
        if condition_1 and condition_2 and condition_3:
            return True
        return False

    def search_horison_or_vert(
                                self, x_coord, y_coord,
                                opponent, mode="horisontal"):
        """
        Start searching in horisontal or vertical mode (modify x or y coord)
        for better accuracy.
        Used while searching fields near last accurate shoot.
        """
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

    def find_field_in_desperado_mode(self, opponent):
        """Search for any field to attack. Iterate over all board."""
        x_coord = 0
        y_coord = 0
        coords = (x_coord, y_coord)
        for row in range(10):
            for column in range(10):
                if self.check_if_new_coords_in_board_and_not_in_memo(
                                                                    x_coord,
                                                                    y_coord):
                    checker = self.was_player_hit(x_coord, y_coord, opponent)
                    coords = (x_coord, y_coord)
                    self.remember_used_coords(coords, checker)
                    if checker:
                        return coords
                y_coord += 1
            x_coord += 1
        return coords
