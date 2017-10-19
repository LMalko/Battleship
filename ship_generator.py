from random import randint, choice


# This board generation function is intended for testing purposes only.
def __generate_board(width=10, height=10, fill_char=" "):
    board = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(fill_char)
        board.append(row)

    return board


def does_ship_fit_within_board_boundaries(board, coords_pair):
    # Coords pair is a [ [x_begin, y_begin], [x_end, y_end] ].
    x_b = coords_pair[0][0]
    y_b = coords_pair[0][1]
    x_e = coords_pair[1][0]
    y_e = coords_pair[1][1]
    # Our board is a rectangle.
    max_x = len(board[0])
    max_y = len(board)
    return 0 <= x_b < max_x and 0 <= x_e < max_x and 0 <= y_b < max_y and 0 <= y_e < max_y


# Returns True if a ship_points_to_be_tested is in direct vicinity of any used_area_points.
def is_ship_at_or_beside_another(used_area_points, ship_points_to_be_tested):
    for point_to_be_tested in ship_points_to_be_tested:
        # We need to test nine points:
        # [x-1, y-1] [x, y-1] [x+1, y-1]
        # [x-1, y  ] [x, y  ] [x+1, y  ]
        # [x-1, y+1] [x, y+1] [x+1, y+1]
        x_b = point_to_be_tested[0]
        y_b = point_to_be_tested[1]
        point_candidates = []
        for x in range(x_b - 1, x_b + 2):
            for y in range(y_b - 1, y_b + 2):
                point_candidates.append([x, y])

        # Check if any candidate point is already used.
        for candidate_pt in point_candidates:
            if any(point == candidate_pt for point in used_area_points):
                return True

    return False


# Internal function, not to be used outside of this module in general...
def __evaluate_start_end_coords_into_point_list(coords_pair):
    ship_points = []
    ship_coords_begin = coords_pair[0]
    ship_coords_end = coords_pair[1]
    if ship_coords_begin[0] == ship_coords_end[0]:
        # X is constant, iterate over y's.
        if ship_coords_begin[1] > ship_coords_end[1]:
            # If begin y is greater than end y, swap begin with end.
            ship_coords_begin, ship_coords_end = ship_coords_end, ship_coords_begin

        for i in range(ship_coords_end[1] - ship_coords_begin[1] + 1):
            ship_points.append([ship_coords_begin[0], ship_coords_begin[1] + i])
    else:
        # Y is constant, iterate over x's.
        if ship_coords_begin[0] > ship_coords_end[0]:
            # If begin x is greater than end x, swap begin with end.
            ship_coords_begin, ship_coords_end = ship_coords_end, ship_coords_begin

        for i in range(ship_coords_end[0] - ship_coords_begin[0] + 1):
            ship_points.append([ship_coords_begin[0] + i, ship_coords_begin[1]])

    return ship_points


def __get_ship_types():
    return {"Carrier": 5, "Battleship": 4, "Cruiser": 3, "Submarine": 3, "Destroyer": 2}


def generate_ship_coords(board, internal_testing=False):
    ships = {}
    ship_count = 0
    ship_type_dict = __get_ship_types()
    amount_distinct_types = len(ship_type_dict)
    # A collection of points occupied by already generated ships.
    used_area_points = []
    while ship_count < amount_distinct_types:
        # Grab a random ship type from our dict.
        ship_key = choice(list(ship_type_dict.keys()))
        ship_length = ship_type_dict[ship_key]
        # Randomize (x_begin, y_begin).
        ship_coords_begin = [randint(0, len(board[0])), randint(0, len(board))]
        # Randomize (x_end, y_end) by adding or subtracting ship length
        # to/ from either the x_begin or y_begin.
        ship_coords_end = ship_coords_begin[:]
        coord_random_index = randint(0, len(ship_coords_end) - 1)
        # Assume addition.
        if(randint(0, 1) == 0):
            ship_coords_end[coord_random_index] += ship_length - 1
        # Assume subtraction.
        else:
            ship_coords_end[coord_random_index] -= ship_length - 1

        ship_start_end_coord_pair = [ship_coords_begin, ship_coords_end]
        if does_ship_fit_within_board_boundaries(board, ship_start_end_coord_pair):
            # Evaluate start-end coordinates to a collection of points.
            ship_points = __evaluate_start_end_coords_into_point_list(ship_start_end_coord_pair)

            # Test the collection against used area.
            if not is_ship_at_or_beside_another(used_area_points, ship_points):
                # Places a copy in dict.
                ships[ship_key] = ship_points[:]
                ship_count += 1
                # Add points of the newly generated ship to the used area.
                for point in ship_points:
                    used_area_points.append(point)
                # Delete this ship from our dictionary.
                del ship_type_dict[ship_key]

    if internal_testing:
        for point in used_area_points:
            board[point[1]][point[0]] = "S"

    return ships


# Function for internal testing.
def __print_board(board):
    for row in board:
        for elem in row:
            print(elem, end="")
        print()
    print()


def main():
    while True:
        print("\n" * 7)
        board = __generate_board()
        ships = generate_ship_coords(board, True)
        __print_board(board)
        for key, value in ships.items():
            print(key.rjust(20, " "), ":", value)

        dummy = input("Press any key to continue")


if __name__ == "__main__":
    main()
