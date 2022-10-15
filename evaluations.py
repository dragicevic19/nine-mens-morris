from gameplay import *
from board import *


def closed_morris(board, last_move, player1, player2):
    if check_for_mill(board, player1, last_move):
        return 1
    else:
        return 0


def num_of_morrises(board, player1, player2):
    num_of_player1_morris = 0
    num_of_player2_morris = 0

    for i in range(24):
        if board[i] == player1:
            num_of_player1_morris += check_for_mill(board, player1, i)
        elif board[i] == player2:
            num_of_player2_morris += check_for_mill(board, player2, i)

    return num_of_player1_morris - num_of_player2_morris


def num_of_blocked_opp_pieces(board, player1, player2):
    blocked_player1_pieces = 0
    blocked_player2_pieces = 0
    for i in range(24):
        if board[i] == player1:
            blocked_player1_pieces += is_blocked_piece(board, i, player2)
        elif board[i] == player2:
            blocked_player2_pieces += is_blocked_piece(board, i, player1)

    return blocked_player2_pieces - blocked_player1_pieces


def is_blocked_piece(board, i, player):
    adjacent_points = nearby_places(i)
    blocked = 0
    for place in adjacent_points:
        if board[place] == player:
            blocked += 1
    if blocked == len(adjacent_points):
        return 1
    else:
        return 0


def num_of_pieces(board, player1, player2):
    num_of_player1_pieces, num_of_player2_pieces = count_pieces(board, player1, player2)
    return num_of_player1_pieces - num_of_player2_pieces


def num_of_2_pieces(board, player1, player2):
    num_of_2_for_player1 = 0
    num_of_2_for_player2 = 0
    for i in range(24):
        if board[i] == 'O':
            num_of_2_for_player1 += count_2_pieces_config(board, i, player1)
            num_of_2_for_player2 += count_2_pieces_config(board, i, player2)

    return num_of_2_for_player1 - num_of_2_for_player2


def count_2_pieces_config(board, i, player):
    board[i] = player
    if check_for_mill(board, player, i):
        board[i] = 'O'
        return 1
    else:
        board[i] = 'O'
        return 0


def num_of_3_pieces(board, player1, player2):
    num_of_3_for_player1 = 0
    num_of_3_for_player2 = 0

    for i in range(24):
        if board[i] == player1:
            if is_three_piece_config(board, i, player1):
                num_of_3_for_player1 += 1
        elif board[i] == player2:
            if is_three_piece_config(board, i, player2):
                num_of_3_for_player2 += 1

    return num_of_3_for_player1 - num_of_3_for_player2


def is_three_piece_config(board, i, player):
    if check_for_mill(board, player, i):
        return False

    adjacent_points = nearby_places(i)
    count = 0
    for place in adjacent_points:
        if board[place] == player:
            count += 1
    if count == 2:
        return True
    return False


def opened_morris(board):
    pass


def double_morris(board, player1, player2):
    num_of_double_morrises = 0
    for i in range(24):
        if board[i] == player1:
            num_of_double_morrises += calculate_double_morris(board, i, player1)
        elif board[i] == player2:
            num_of_double_morrises += calculate_double_morris(board, i, player2)
    return num_of_double_morrises


def calculate_double_morris(board, i, player):
    morris_count = 0
    adjacent_points = nearby_places(i)
    for point in adjacent_points:
        if check_for_mill(board, player, point):
            morris_count += 1
    if morris_count == 2:
        return 1
    return 0


def winning_configuration(board, player1, player2):
    remaining_player1_pieces, remaining_player2_pieces = count_pieces(board, player1, player2)

    if remaining_player2_pieces < 3:
        return 1
    elif remaining_player1_pieces < 3:
        return -1
    elif num_of_blocked(board, player2) == remaining_player2_pieces:
        return 1
    elif num_of_blocked(board, player1) == remaining_player1_pieces:
        return -1
    else:
        return 0


def count_pieces(board, player1, player2):
    remaining_player1_pieces = 0
    remaining_player2_pieces = 0
    try:
        for i in range(24):
            if board[i] == player1:
                remaining_player1_pieces += 1
            elif board[i] == player2:
                remaining_player2_pieces += 1

    except IndexError:  # desi se kada pojedem figuru a ostale figure ostanu blokirane (vise od 3 figure)
        if player1 == 'W':
            remaining_player2_pieces = 2
        elif player1 == 'B':
            remaining_player1_pieces = 2

    return remaining_player1_pieces, remaining_player2_pieces


def num_of_blocked(board, player):
    count_blocked = 0
    for i in range(24):
        if board[i] == player:
            count_blocked += is_blocked_piece(board, i, player)
    return count_blocked


def phase_one_relations(board, player1):
    if player1:
        player1 = 'W'
        player2 = 'B'
    else:
        player1 = 'B'
        player2 = 'W'

    evaluation = 0
    # evaluation += 18 * closed_morris(board, player1, ,player2)
    evaluation += 26 * num_of_morrises(board, player1, player2)
    evaluation += 1 * num_of_blocked_opp_pieces(board, player1, player2)
    evaluation += 9 * num_of_pieces(board, player1, player2)
    evaluation += 10 * num_of_2_pieces(board, player1, player2)
    evaluation += 7 * num_of_3_pieces(board, player1, player2)
    return evaluation


def phase_23_relations(board, player1):
    if player1:
        player_one = 'W'
        player_two = 'B'
    else:
        player_one = 'B'
        player_two = 'W'

    rem_pieces_player1, rem_pieces_player2 = count_pieces(board, player_one, player_two)

    if rem_pieces_player1 == 3:
        evaluation = phase_three_relations(board, player1)
    else:
        evaluation = phase_two_relations(board, player1)

    return evaluation


def phase_two_relations(board, player1):
    if player1:
        player1 = 'W'
        player2 = 'B'
    else:
        player1 = 'B'
        player2 = 'W'

    evaluation = 0
    # evaluation += 14 * closed_morris(board, player1, player2)
    evaluation += 43 * num_of_morrises(board, player1, player2)
    evaluation += 10 * num_of_blocked_opp_pieces(board, player1, player2)
    evaluation += 10 * num_of_pieces(board, player1, player2)
    evaluation += 8 * double_morris(board, player1, player2)
    evaluation += 1086 * winning_configuration(board, player1, player2)
    return evaluation


def phase_three_relations(board, player1):
    if player1:
        player1 = 'W'
        player2 = 'B'
    else:
        player1 = 'B'
        player2 = 'W'

    evaluation = 0
    # evaluation += 16 * closed_morris(board)
    evaluation += 43 * num_of_morrises(board, player1, player2)
    evaluation += 10 * num_of_2_pieces(board, player1, player2)
    evaluation += 1 * num_of_3_pieces(board, player1, player2)
    evaluation += 1190 * winning_configuration(board, player1, player2)
    return evaluation
