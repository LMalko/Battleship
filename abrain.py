"""This module contain AI mechanic."""

import random


class ABrain():
    """Abstract class with attribs and methods used in class AI(Player)."""
    # Ai_memo (dict) contains coordinates of all past ai shots and results:
    # key = coords, value = bool (True if shot was accurate and ship wasn't sunk yet).
    ai_memo = {}
    last_accurate_coords = ()
    # Intelligence (integer) specify ai accuracy in shooting enemy ships depends on game difficulty_lvl.
    intelligence = 1
    # Should_search_... is part of ai memory, which has influence on ai choices.
    should_search_horizontal = False
    should_search_vertical = False

    def search_and_try_destroy(self, opponent):
        """Start searching & shooting process, returns coordinates."""
        # If the last accurate shot was not long ago.
        if self.__check_if_bother_last_accurate_coords(opponent):
            # Try in ocean_fields in neighborhood,
            coords = self.__check_coords_next_to(opponent)
        else:
            # or try in new ocean_fields.
            coords = self.__check_new_coords(opponent)
        return coords

    def __was_player_hit(self, x_coord, y_coord, opponent):
        """Check if opponent's ship was hit, returns bool."""
        was_square_used_before = opponent.board.ocean_fields[x_coord][y_coord].single_square_hit_count == 0
        is_ship_on_square = opponent.board.ocean_fields[x_coord][y_coord].associated_class_obj
        if was_square_used_before and is_ship_on_square:
            self.last_accurate_coords = (x_coord, y_coord)
            return True
        return False

    def __check_new_coords(self, opponent):
        """Return attack coordinates."""
        if self.intelligence == 3:
            tries_modifier = 1
        else:
            tries_modifier = 0
        tries_number = self.intelligence + tries_modifier
        # Starting tmp coords.
        coords = (10, 10)
        for tries in range(tries_number):
            for check in range(40):
                x_coord = random.randint(0, 9)
                y_coord = random.randint(0, 9)
                if self.__check_if_new_coords_in_board_and_not_in_memo(
                                                                    x_coord,
                                                                    y_coord):

                    break
            checker = self.__was_player_hit(x_coord, y_coord, opponent)
            coords = (x_coord, y_coord)
            self.__remember_used_coords(coords, checker)
            if checker:
                return coords
        # If can't find any unused field to attack.
        if coords == (10, 10):
            coords = self.__find_field_in_desperado_mode(opponent)
        return coords

    def __check_coords_next_to(self, opponent):
        """Return tuple with coords."""
        while True:
            x_coord = self.last_accurate_coords[0]
            y_coord = self.last_accurate_coords[1]
            if (self.should_search_vertical or self.should_search_horizontal) and self.intelligence > 1:
                if self.should_search_vertical:
                    coords = self.__search_horizon_or_vert(
                                                        x_coord, y_coord,
                                                        opponent,
                                                        mode="vertical")
                else:
                    coords = self.__search_horizon_or_vert(
                                                        x_coord, y_coord,
                                                        opponent,
                                                        mode="horizontal")
            else:
                decide_if_horizontal = random.choice((True, False))
                if decide_if_horizontal:
                    coords = self.__search_horizon_or_vert(
                                                        x_coord, y_coord,
                                                        opponent,
                                                        mode="horizontal")
                else:
                    coords = self.__search_horizon_or_vert(
                                                        x_coord, y_coord,
                                                        opponent,
                                                        mode="vertical")
            if coords:
                return coords

    def __check_if_bother_last_accurate_coords(self, opponent):
        """Check if it makes sense to relate to last accurate shot. Returns bool."""
        if self.last_accurate_coords:
            if self.__is_ship_alive(opponent):
                return True
        return False

    def __remember_used_coords(self, coords, checker):
        """Save result of last shot in memory."""
        if coords not in self.ai_memo:
            self.ai_memo[(coords)] = checker

    def __forget_horizon_and_vertical(self):
        """Forget should_search_horizontal & should_search_vertical."""
        self.should_search_horizontal = False
        self.should_search_vertical = False

    def __check_if_new_coords_in_board_and_not_in_memo(self, x_coord, y_coord):
        """
        Take coordinates and check if they're not in memory (so they're fresh).

        Check if coordinates are in correct range (0, 9).
        Reason: AI can save them as new result. Returns bool.
        """
        condition_1 = x_coord in range(0, 9)
        condition_2 = y_coord in range(0, 9)
        condition_3 = (x_coord, y_coord) not in self.ai_memo
        if condition_1 and condition_2 and condition_3:
            return True
        return False

    def __search_horizon_or_vert(self, x_coord, y_coord, opponent, mode="horizontal"):
        """
        Start searching in horizontal or vertical mode.

        (modify x or y coord) for better accuracy.
        Used while searching ocean_fields near last accurate shoot.
        """
        coords = False
        if mode == "horizontal":
            coord = y_coord
        else:
            coord = x_coord
        for num in (-1, 2):
            coord += num
            if mode == "horizontal":
                y_coord = coord
            else:
                x_coord = coord
            if self.__check_if_new_coords_in_board_and_not_in_memo(
                                                            x_coord,
                                                            y_coord):
                checker = self.__was_player_hit(
                                                x_coord,
                                                y_coord, opponent)
                coords = (x_coord, y_coord)
                self.__remember_used_coords(coords, checker)
                if checker:
                    if mode == "horizontal":
                        self.should_search_horizontal = True
                    else:
                        self.should_search_vertical = True
                    return coords
        if coords is False:
            self.__update_last_accurate_coords(opponent)
        return coords

    def __find_field_in_desperado_mode(self, opponent):
        """Search for any field to attack. Iterate over all board."""
        x_coord = 0
        y_coord = 0
        coords = (x_coord, y_coord)
        for row in range(10):
            for column in range(10):
                if self.__check_if_new_coords_in_board_and_not_in_memo(
                                                                    x_coord,
                                                                    y_coord):
                    checker = self.__was_player_hit(x_coord, y_coord, opponent)
                    coords = (x_coord, y_coord)
                    self.__remember_used_coords(coords, checker)
                    if checker:
                        return coords
                y_coord += 1
            x_coord += 1
        return coords

    def __is_ship_alive(self, opponent):
        x_coord = self.last_accurate_coords[0]
        y_coord = self.last_accurate_coords[1]
        try:
            ship_is_alive = opponent.board.ocean_fields[x_coord][y_coord].associated_class_obj.hit_points > 0
            if ship_is_alive:
                return True
        except:
            self.__forget_horizon_and_vertical()
            return False
        self.__forget_horizon_and_vertical()
        return False

    def __update_last_accurate_coords(self, opponent):
        x_coord = self.last_accurate_coords[0]
        y_coord = self.last_accurate_coords[1]
        all_accurate_coords = [coords for coords in self.ai_memo if self.ai_memo[coords] is True]
        try:
            targeted_ship_max_hp = opponent.board.ocean_fields[x_coord][y_coord].associated_class_obj.max_hit_points
            targeted_ship_hp_left = opponent.board.ocean_fields[x_coord][y_coord].associated_class_obj.hit_points
            coords_updater_index = targeted_ship_max_hp - targeted_ship_hp_left
            self.last_accurate_coords = all_accurate_coords[-coords_updater_index]
        except:
            pass
