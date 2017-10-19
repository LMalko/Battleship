# Battleship in the OOP way

## The story

In 2005, scientists discover in the Gliese system (some 23 light years from Earth) an extrasolar planet, which is named Planet G, believed to be the closest planet to Earth having conditions nearly identical to Earth. In 2006, NASA completes the construction of a transmission device in Hawaii that is five times more powerful than any before it, and a program to contact the planet, known as The Beacon Project, begins.

In 2012, YOU are a hothead and disrespectful lieutenant and Tactical Action Officer aboard the Arleigh Burke-class destroyer USS John Paul Jones, YOU hold the rank of commander and the Commanding Officer of USS Sampson. YOUR ships join the 2012 Rim of the Pacific Exercise (RIMPAC) in Hawaii. During the exercises, five alien spacecraft arrive in response to the NASA signal (no explanation is given as to how these spacecraft cross 23 light years in a matter of hours). Their communications ship collides with a satellite and crashes in Hong Kong, causing heavy casualties and damage while the other four (a mothership and three warships) land in the water near the coast of Hawaii. 

YOU are ordered to investigate. Upon arrival at the indicated location, they discover a massive dormant floating structure. YOU and two crew members, JERZY and JERZY'S BROTHER, are sent to approach the structure in an armed Zodiac.

When YOU touche the structure, it knocks YOU away and generates a massive force field that encloses the Hawaiian Islands, separating the Navy ships from the RIMPAC fleet. The warships emerge from beneath the water and face the Navy ships in a defensive posture. 



Under JERZY'S orders, YOU begin a game of battleship. 


## Specification

__main.py__

Creates GameFlow instance.

	Functions:

	delay_print(string):None
	main():None

__game_flow.py__#
class GameFlow()

	Methods:

__abrain.py__#
class ABrain()

	Methods:

__ocean.py__#
class Ocean()

	Methods:

__player.py__#
class Player()

	Methods:

class Human(Player)

	Methods:

class AI(Player, AI)

	Methods:

__quiz.py__

	Functions:

	summary(correct_answers_count):None
	quiz_flow(questions, answers):None
	start():None

__ship_generator.py__

	Functions:

	__generate_board(width = 10, height = 10, fill_char = " "):list
	does_ship_fit_within_board_boundaries(board, coords_pair):int
	is_ship_at_or_beside_another(used_area_points, ship_points_to_be_tested):bool
	__evaluate_start_end_coords_into_point_list(coords_pair):list
	__get_ship_types():dict
	generate_ship_coords(board, internal_testing = False):dict
	__print_board(board):None
	main():None

__ship_position_picker.py__

	Functions:

	getch_single_character():
	getch_two_characters():
	handle_origin_movement(board, direction, origin_char, origin_pos, old_origin_character):str
	overwrite_board(left, right, coords):list
	overlay_board(board, layer):list
	bind_maps_horz(left, right):list
	set_message(msg_board, message):None
	get_predefined_color(color):dict
	adjust_points_color(board, ship_points, start_end_coords, direction_key, directed_colors, used_area_points):None
	lay_ghost_points(layer, points, fill_char, direction_key, directed_colors, board_offset):None
	get_painted_layer_with_ghost_ships(board, sandbox, origin_coords, board_offset, ship_length,     						   chosen_direction,used_area_points,possible_ship_directions):list
	colored_string(string, color):str
	message_is_possible_to_place_ship(preferred_direction, possible_ship_directions):str
	handle_arrows(user_input, preferred_direction, possible_ship_directions):obj
	handle_tab(ship_keys_ordered, ship_types, current_ship_type_index):str
	handle_enter(board,preferred_direction,possible_ship_directions,ship_types,ship_keys_ordered,used_area_points,
    		     current_ship_type_index,created_ships,old_origin_character):str
	draw_sandbox_row_col_marks(sandbox, board_offset):None
	get_ship_dictionary_from_user_input():None
	main():None

__ship.py__#

Methods:

__square.py__#

Methods:



