import sys
import os
import tty
import termios
import ship_generator


def getch_single_character():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def getch_two_characters():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def handle_origin_movement(
        board,
        direction,
        origin_char,
        origin_pos,
        old_origin_character
        ):
    dx = 0
    dy = 0
    if direction == "w":
        # Up, decrement y.
        dy = -1
    elif direction == "s":
        # Down, increment y.
        dy = 1
    elif direction == "a":
        # Left, decrement x.
        dx = -1
    elif direction == "d":
        # Right, increment x.
        dx = 1

    x_new = origin_pos[0] + dx
    y_new = origin_pos[1] + dy
    new_pos = [x_new, y_new]

    is_new_pos_within_board = \
        0 <= y_new < len(board) and \
        0 <= x_new < len(board[y_new])

    if not is_new_pos_within_board:
        return "Prevented from going out of bounds..."
    else:  # Perform the move restore previous character to old position.
        board[origin_pos[1]][origin_pos[0]] = old_origin_character[0]
        # Save character to be stepped at for restoration.
        old_origin_character[0] = board[new_pos[1]][new_pos[0]]
        # Move/ `draw` origin character in new pos.
        board[new_pos[1]][new_pos[0]] = origin_char
        # Update char_pos to the outside world.
        origin_pos[0] = x_new
        origin_pos[1] = y_new
        return ""


def overwrite_board(left, right, coords):
    ''' Writes right board on top of left, starting at coords.'''
    x_begin = coords[0]
    y_begin = coords[1]
    for dy in range(len(right)):
        for dx in range(len(right[dy])):
            left[y_begin + dy][x_begin + dx] = right[dy][dx]

    return left


def overlay_board(board, layer):
    layered_board = []
    for y in range(len(board)):
        row = []
        for x in range(len(board[y])):
            row.append(board[y][x])
        layered_board.append(row)

    dimensions_equal = len(board) == len(layer) and len(board[0]) == len(layer[0])
    if not dimensions_equal:
        raise ValueError("board and layer dimensions mismatch")

    for y in range(len(layer)):
        for x in range(len(layer[y])):
            if layer[y][x] is not None:
                layered_board[y][x] = layer[y][x]

    return layered_board


def bind_maps_horz(left, right):
    ''' Returns a bound map of 2 maps in horizontal orientation.'''
    left_indent = [" "] * len(left[0])
    bound = []
    if len(right) > len(left):
        for i in range(len(right)):
            if i < len(left):
                bound.append(left[i] + right[i])
            else:
                bound.append(left_indent + right[i])
    else:
        for i in range(len(left)):
            if i < len(right):
                bound.append(left[i] + right[i])
            else:
                bound.append(left[i])

    return bound


def set_message(msg_board, message):
    # Wipe message board.
    for y in range(len(msg_board)):
        for x in range(len(msg_board[y])):
            msg_board[y][x] = " "

    for i, subline in enumerate(message.split("\n")):
        input_idx = 0
        output_idx = 0
        while input_idx < len(subline):
            # Escape sequence begin?
            if subline[input_idx] == "\x1b":
                # take escape + 2 next characters => color
                color_seq = subline[input_idx:input_idx+5] + " "
                msg_board[i+1][output_idx] = color_seq
                input_idx += 5
            else:
                msg_board[i+1][output_idx] = subline[input_idx]
                input_idx += 1

            output_idx += 1


def get_predefined_color(color):
    colors = {
        "black": "\x1b[30m",
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "orange": "\x1b[33m",
        "blue": "\x1b[34m",
        "purple": "\x1b[35m",
        "cyan": "\x1b[36m",
        "lightgrey": "\x1b[37m",
        "darkgrey": "\x1b[90m",
        "lightred": "\x1b[91m",
        "lightgreen": "\x1b[92m",
        "yellow": "\x1b[93m",
        "lightblue": "\x1b[94m",
        "pink": "\x1b[95m",
        "lightcyan": "\x1b[96m",
        "default": "\x1b[0m"
    }
    if color not in colors:
        raise KeyError("invalid color specifier")

    return colors[color]


def adjust_points_color(board, ship_points, start_end_coords, direction_key, directed_colors, used_area_points):
    if ship_generator.does_ship_fit_within_board_boundaries(board, start_end_coords):
        if not ship_generator.is_ship_at_or_beside_another(used_area_points, ship_points):
            directed_colors[direction_key] = get_predefined_color("green")


def lay_ghost_points(layer, points, fill_char, direction_key, directed_colors, board_offset):
    default_color = get_predefined_color("default")
    for point in points:
        x = point[0] + board_offset[0]
        y = point[1] + board_offset[1]
        layer[y][x] = directed_colors[direction_key] + fill_char + default_color


# returns a layer the size of sandbox
# layer differs from a board in that most of its items are NoneType
# and only non-None elements are `laid` on top of a board
# WITHOUT modifying the board itself
# board is the main game board
# sandbox is an extended board with board drawn at the center, it is used to demonstrate
# how a would-be ship would look like if it were placed on board
def get_painted_layer_with_ghost_ships(
        board,
        sandbox,
        origin_coords,
        board_offset,
        ship_length,
        chosen_direction,
        used_area_points,
        possible_ship_directions
        ):
    blurred_solid_block = u"\u2591"
    solid_solid_block = u"\u2593"
    solid_sequence_length = 0
    if ship_length is not None:
        # We don't count in the origin, hence the decrement.
        solid_sequence_length = ship_length - 1

    # Create an empty layer.
    layer = []
    for y in range(len(sandbox)):
        row = []
        for x in range(len(sandbox[y])):
            row.append(None)
        layer.append(row)

    # Don't generate ghost ships if there are no more ships.
    if solid_sequence_length == 0:
        return layer

    preferred_direction = chosen_direction[0]
    x = origin_coords[0]
    y = origin_coords[1]
    # Create coordinate pairs of ghost/ would-be ships.
    west_option = [[x - solid_sequence_length, y], [x - 1, y]]
    east_option = [[x + 1, y], [x + solid_sequence_length, y]]
    north_option = [[x, y - solid_sequence_length], [x, y - 1]]
    south_option = [[x, y + 1], [x, y + solid_sequence_length]]

    # Evaluate start-end coordinate pairs into point collections.
    west_points = ship_generator.__evaluate_start_end_coords_into_point_list(west_option)
    east_points = ship_generator.__evaluate_start_end_coords_into_point_list(east_option)
    north_points = ship_generator.__evaluate_start_end_coords_into_point_list(north_option)
    south_points = ship_generator.__evaluate_start_end_coords_into_point_list(south_option)

    red = get_predefined_color("lightred")
    green = get_predefined_color("green")
    # Assume all possibilities `red`, i.e. disallowed.
    directed_colors = {"West": red, "East": red, "North": red, "South": red}

    # Adjust_points_color sets direction color to green if these two conditions are met:
    # All ship points lie within board boundaries.
    # None of ship points are at or directly beside any others' points.
    adjust_points_color(board, west_points, west_option, "West", directed_colors, used_area_points)
    adjust_points_color(board, east_points, east_option, "East", directed_colors, used_area_points)
    adjust_points_color(board, north_points, north_option, "North", directed_colors, used_area_points)
    adjust_points_color(board, south_points, south_option, "South", directed_colors, used_area_points)
    # Put the points onto the layer.
    fill_block = solid_solid_block if preferred_direction == "left" else blurred_solid_block
    lay_ghost_points(layer, west_points, fill_block, "West", directed_colors, board_offset)

    fill_block = solid_solid_block if preferred_direction == "right" else blurred_solid_block
    lay_ghost_points(layer, east_points, fill_block, "East", directed_colors, board_offset)

    fill_block = solid_solid_block if preferred_direction == "up" else blurred_solid_block
    lay_ghost_points(layer, north_points, fill_block, "North", directed_colors, board_offset)

    fill_block = solid_solid_block if preferred_direction == "down" else blurred_solid_block
    lay_ghost_points(layer, south_points, fill_block, "South", directed_colors, board_offset)

    # Update possible_ships_dict.
    # Adjust start-end ghost ship coordinates to include origin.
    west_option[1] = origin_coords
    east_option[0] = origin_coords
    north_option[1] = origin_coords
    south_option[0] = origin_coords

    # Re-generate points to include origin.
    west_points = ship_generator.__evaluate_start_end_coords_into_point_list(west_option)
    east_points = ship_generator.__evaluate_start_end_coords_into_point_list(east_option)
    north_points = ship_generator.__evaluate_start_end_coords_into_point_list(north_option)
    south_points = ship_generator.__evaluate_start_end_coords_into_point_list(south_option)

    possible_ship_directions["left"] = [False if directed_colors["West"] == red else True, west_points]
    possible_ship_directions["right"] = [False if directed_colors["East"] == red else True, east_points]
    possible_ship_directions["up"] = [False if directed_colors["North"] == red else True, north_points]
    possible_ship_directions["down"] = [False if directed_colors["South"] == red else True, south_points]

    return layer


def colored_string(string, color):
    return get_predefined_color(color) + string + get_predefined_color("default")


def message_is_possible_to_place_ship(preferred_direction, possible_ship_directions):
    if possible_ship_directions[preferred_direction[0]][0]:
        # The ship can be placed.
        return colored_string("You can set ship here.", "green") \
        + "\n\n Press Enter to save the ship\n at this position."
    else:
        return colored_string("You can't set ship here.", "lightred") \
        + "\n\n Change direction using arrows\n or move origin with WSAD somewhere else."


def handle_arrows(user_input, preferred_direction, possible_ship_directions):
    UP_ARROW = "\x1b[A"
    DOWN_ARROW = "\x1b[B"
    LEFT_ARROW = "\x1b[D"
    RIGHT_ARROW = "\x1b[C"

    if user_input == UP_ARROW:
        preferred_direction[0] = "up"

    elif user_input == DOWN_ARROW:
        preferred_direction[0] = "down"

    elif user_input == RIGHT_ARROW:
        preferred_direction[0] = "right"

    elif user_input == LEFT_ARROW:
        preferred_direction[0] = "left"

    return message_is_possible_to_place_ship(preferred_direction, possible_ship_directions)


def handle_tab(ship_keys_ordered, ship_types, current_ship_type_index):
    if len(ship_keys_ordered):
        current_ship_type_index[0] = (current_ship_type_index[0]+1) % len(ship_keys_ordered)
        particular_type = ship_keys_ordered[current_ship_type_index[0]]
        return " Currently selected ship type:\n" + \
            colored_string("    %s (weight: %u)" % (particular_type, ship_types[particular_type]), "yellow")
    else:
        return " Currently selected ship type:\n    " + colored_string("None", "orange")


def handle_enter(
        board,
        preferred_direction,
        possible_ship_directions,
        ship_types,
        ship_keys_ordered,
        used_area_points,
        current_ship_type_index,
        created_ships,
        old_origin_character
        ):
    if possible_ship_directions[preferred_direction[0]][0]:
        # the preferred direction is viable
        ship_points = possible_ship_directions[preferred_direction[0]][1]
        current_ship_type = ship_keys_ordered[current_ship_type_index[0]]
        # add points to used/ disallowed-for-further-use area
        for pt in ship_points:
            used_area_points.append(pt)

        coords_transposed = []
        # create a list of `transposed` coordinates
        for i in range(len(ship_points)):
            coords_transposed.append([ship_points[i][1], ship_points[i][0]])
        created_ships[current_ship_type] = coords_transposed

        # mark the chosen ship on board
        used_area_fill_block = colored_string(u"\u2593", "orange")
        for pt in ship_points:
            x = pt[0]
            y = pt[1]
            board[y][x] = used_area_fill_block
        # prevent motion handling loop from restoring the former default
        # block by tricking it into thinking that a colorful block had been there
        old_origin_character[0] = used_area_fill_block
        # remove ship from our choice dictionary
        del ship_types[current_ship_type]
        # update list of ship type keys
        new_ship_keys = sorted(list(ship_types.keys()))
        # delete old keys
        for i in reversed(range(len(ship_keys_ordered))):
            del ship_keys_ordered[i]
        # append new
        for i in range(len(new_ship_keys)):
            ship_keys_ordered.append(new_ship_keys[i])

        current_ship_type_index[0] = 0
        return colored_string("Added %s, length: %u" % (current_ship_type, len(ship_points)), "cyan")
    else:
        return ""


def draw_sandbox_row_col_marks(sandbox, board_offset):
    # draw column numbers
    col_num_start_coord = [board_offset[0], board_offset[1] - 2]
    col_x = col_num_start_coord[0]
    col_y = col_num_start_coord[1]
    for i in range(10):
        # Two characters.
        if i + 1 == 10:
            numstr = str(i+1)
            # First character.
            sandbox[col_y][col_x + i] = \
                numstr[0] if i % 2 == 0 else \
                colored_string(numstr[0], "lightblue")
            # Second character.
            sandbox[col_y][col_x + i + 1] = \
                numstr[1] if i % 2 == 0 else \
                colored_string(numstr[1], "lightblue")
        else:
            # Single character.
            sandbox[col_y][col_x + i] = \
                str(i+1) if i % 2 == 0 else \
                colored_string(str(i+1), "lightblue")

    # Draw row marks.
    row_mark_start_coord = [board_offset[0] - 2, board_offset[1]]
    row_x = row_mark_start_coord[0]
    row_y = row_mark_start_coord[1]
    for i in range(10):
        sandbox[row_y + i][row_x] = \
            chr(ord("A") + i) if i % 2 == 0 else \
            colored_string(chr(ord("A") + i), "lightblue")


def get_ship_dictionary_from_user_input():
    board = ship_generator.__generate_board(10, 10)
    sandbox_fillchar = colored_string(u"\u2591", "lightgrey")
    sandbox = ship_generator.__generate_board(21, 21, sandbox_fillchar)
    message_board = ship_generator.__generate_board(70, 21)
    for dx in range(len(sandbox[0])):
        sandbox[0][dx] = " "

    for dy in range(len(sandbox)):
        sandbox[dy][0] = " "

    origin_pos = [5, 5]
    movement_specifiers = ("w", "s", "a", "d")
    TAB = 9
    ENTER = 13
    SPACE = 32
    ESCAPE = 27

    UP_ARROW = "\x1b[A"
    DOWN_ARROW = "\x1b[B"
    LEFT_ARROW = "\x1b[D"
    RIGHT_ARROW = "\x1b[C"
    arrows = (UP_ARROW, DOWN_ARROW, LEFT_ARROW, RIGHT_ARROW)

    # Default value for ghost ship suggestion.
    preferred_direction = ["up"]
    # Possible_ship_directions holds something like this:
    # "up": [ True, [ ship points ] ]
    # a boolean indicates whether [ship points] are valid and can be used.
    possible_ship_directions = {}

    ship_types = ship_generator.__get_ship_types()
    ship_keys_ordered = sorted(list(ship_types.keys()))
    current_ship_type_index = [0]
    origin_char = colored_string(u"\u2588", "default")
    # Save the character at which origin character will be placed; it will be restored after a move.
    old_origin_character = [board[origin_pos[1]][origin_pos[0]]]
    board[origin_pos[1]][origin_pos[0]] = origin_char

    used_area_points = []
    board_offset = [6, 6]

    draw_sandbox_row_col_marks(sandbox, board_offset)

    created_ships = {}
    can_set_ship_msg = ""
    aux_msg = "Use WSAD to move origin.\n\n Use arrows to choose ship position."
    output_msg = ""
    # Imitate Tab press for initially selected ship type to appear.
    ship_type_msg = handle_tab(ship_keys_ordered, ship_types, current_ship_type_index)
    while True:
        os.system("clear")

        # Update ghost layer.
        ship_length_argument = None
        if ship_types:
            ship_length_argument = ship_types[ship_keys_ordered[current_ship_type_index[0]]]
        # Ghost layer is a board with bare ghost ship outlines, it is laid on top
        # of a board only where its elements are not NoneType.
        ghost_layer = get_painted_layer_with_ghost_ships(
            board,
            sandbox,
            origin_pos,
            board_offset,
            ship_length_argument,
            preferred_direction,
            used_area_points,
            possible_ship_directions)

        if "None" in ship_type_msg:
            can_set_ship_msg = "[all ships have been placed]"
        else:
            can_set_ship_msg = message_is_possible_to_place_ship(
                preferred_direction,
                possible_ship_directions)

        output_msg = ship_type_msg + "\n\n " + can_set_ship_msg + "\n\n " + aux_msg
        set_message(message_board, output_msg)

        # Combine sandbox board with board.
        combined_sandbox_board = overwrite_board(sandbox, board, board_offset)
        # Overlay ghost_layer on top of that composition.
        layered = overlay_board(combined_sandbox_board, ghost_layer)
        # Print a horizontal bind of the above board with message board.
        ship_generator.__print_board(bind_maps_horz(layered, message_board))

        aux_msg = ""
        if not ship_types:
            # We've exhausted ship choice, all the available ships have been placed.
            return created_ships

        # Take one character from input.
        user_input = getch_single_character()
        if ord(user_input) == ESCAPE:
            # We've probably got an arrow press which takes 3 bytes, take another 2.
            user_input += getch_two_characters()

        # Check input.
        if ord(user_input[0]) == TAB:
            ship_type_msg = handle_tab(ship_keys_ordered, ship_types, current_ship_type_index)

        elif ord(user_input[0]) == ENTER:
            aux_msg = handle_enter(board,
                                   preferred_direction,
                                   possible_ship_directions,
                                   ship_types,
                                   ship_keys_ordered,
                                   used_area_points,
                                   current_ship_type_index,
                                   created_ships,
                                   old_origin_character)

            if aux_msg:
                # if auxiliary message is not empty, a ship was added
                # => Tab press simulation is necessary
                ship_type_msg = handle_tab(
                    ship_keys_ordered,
                    ship_types,
                    current_ship_type_index)

        elif user_input in arrows:
            can_set_ship_msg = handle_arrows(
                user_input,
                preferred_direction,
                possible_ship_directions)

        elif user_input[0].lower() in movement_specifiers:
            handle_origin_movement(
                board, user_input[0].lower(), origin_char,
                origin_pos, old_origin_character)


def main():
    ships = get_ship_dictionary_from_user_input()
    for key in ships:
        print(key.rjust(20), ships[key])


if __name__ == "__main__":
    main()
