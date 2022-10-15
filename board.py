from os import system


def make_board(board):
    for key in range(24):
        board[key] = 'O'


def print_board(board):
    # system('clear')
    print(board[0] + "(00)----------------------" + board[1] + "(01)----------------------" + board[2] + "(02)")
    print("|                           |                           |")
    print("|       " + board[8] + "(08)--------------" + board[9] + "(09)--------------" + board[10] + "(10)     |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       |        " + board[16] + "(16)-----" + board[17] + "(17)-----" + board[18] + "(18)       |      |")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print(board[3] + "(03)---" + board[11] + "(11)----" + board[19] + "(19)               " + board[20] + "(20)----" +
          board[12] + "(12)---" + board[4] + "(04)")
    print("|       |         |                   |          |      |")
    print("|       |         |                   |          |      |")
    print("|       |        " + board[21] + "(21)-----" + board[22] + "(22)-----" + board[23] + "(23)       |      |")
    print("|       |                   |                    |      |")
    print("|       |                   |                    |      |")
    print("|       " + board[13] + "(13)--------------" + board[14] + "(14)--------------" + board[15] + "(15)     |")
    print("|                           |                           |")
    print("|                           |                           |")
    print(board[5] + "(05)----------------------" + board[6] + "(06)----------------------" + board[7] + "(07)\n")


#
# def print_board1(board):
#     print(board[0] + "(00)----------------------" + board[1] + "(01)----------------------" + board[2] + "(02)")
#     print("|                           |                           |")
#     print("|       " + board[8] + "(03)--------------" + board[9] + "(04)--------------" + board[10] + "(5)     |")
#     print("|       |                   |                    |      |")
#     print("|       |                   |                    |      |")
#     print("|       |        " + board[16] + "(6)-----" + board[17] + "(7)-----" + board[18] + "(8)       |      |")
#     print("|       |         |                   |          |      |")
#     print("|       |         |                   |          |      |")
#     print(board[3] + "(09)---" + board[11] + "(10)----" + board[19] + "(11)               " + board[20] + "(12)----" +
#           board[12] + "(13)---" + board[4] + "(14)")
#     print("|       |         |                   |          |      |")
#     print("|       |         |                   |          |      |")
#     print("|       |        " + board[21] + "(15)-----" + board[22] + "(16)-----" + board[23] + "(17)       |      |")
#     print("|       |                   |                    |      |")
#     print("|       |                   |                    |      |")
#     print("|       " + board[13] + "(18)--------------" + board[14] + "(19)--------------" + board[15] + "(20)     |")
#     print("|                           |                           |")
#     print("|                           |                           |")
#     print(board[5] + "(21)----------------------" + board[6] + "(22)----------------------" + board[7] + "(23)\n")

def check_user_play(board, user_play):
    try:
        if board[user_play] != 'O':
            return False
        else:
            board[user_play] = 'W'
            return True
    except KeyError:
        return False


def check_user_play_phase23(board, old, new, is_phase3, player):
    try:
        if board[old] != player or board[new] != 'O':
            return False
        elif not is_phase3 and new not in nearby_places(old):
            return False
        else:
            board[old] = 'O'
            board[new] = player
            return True
    except:
        return False


def nearby_places(user_play):
    nearby_locations = [
        [1, 3],
        [0, 2, 9],
        [1, 4],
        [0, 5, 11],
        [2, 7, 12],
        [3, 6],
        [5, 7, 14],
        [4, 6],
        [9, 11],
        [1, 8, 10, 17],
        [9, 12],
        [3, 8, 13, 19],
        [4, 10, 15, 20],
        [11, 14],
        [6, 13, 15, 22],
        [12, 14],
        [17, 19],
        [9, 16, 18],
        [17, 20],
        [11, 16, 21],
        [12, 18, 23],
        [19, 22],
        [21, 23, 14],
        [20, 22]
    ]
    return nearby_locations[user_play]


def check_for_mill(board, player_color, user_play):
    mill = [
        [[1, 2], [3, 5]],
        [[0, 2], [9, 17]],
        [[0, 1], [4, 7]],
        [[0, 5], [11, 19]],
        [[2, 7], [12, 20]],
        [[0, 3], [6, 7]],
        [[5, 7], [14, 22]],
        [[2, 4], [5, 6]],
        [[9, 10], [11, 13]],
        [[8, 10], [1, 17]],
        [[8, 9], [12, 15]],
        [[3, 19], [8, 13]],
        [[20, 4], [10, 15]],
        [[8, 11], [14, 15]],
        [[13, 15], [6, 22]],
        [[13, 14], [10, 12]],
        [[17, 18], [19, 21]],
        [[1, 9], [16, 18]],
        [[16, 17], [20, 23]],
        [[16, 21], [3, 11]],
        [[12, 4], [18, 23]],
        [[16, 19], [22, 23]],
        [[6, 14], [21, 23]],
        [[18, 20], [21, 22]],
    ]

    nearby_locations = mill[user_play]
    for list_of_locations in nearby_locations:
        player_pieces = 0
        for location in list_of_locations:
            if board[location] == player_color:
                player_pieces += 1
        if player_pieces == 2:
            return True

    return False


def check_for_removing_piece(board, remove_piece, player_color):
    if player_color == 'W':
        player2 = 'B'
    else:
        player2 = 'W'
    if board[remove_piece] != player2:
        return False
    else:
        mill_exist = check_for_mill(board, player2, remove_piece)
        if mill_exist:

            from evaluations import count_pieces
            player1_pieces, player2_pieces = count_pieces(board, player_color, player2)

            if player2_pieces == pieces_in_mill(board, player2):
                board[remove_piece] = 'O'
                return board
            return False

        else:
            board[remove_piece] = 'O'
            return board


def pieces_in_mill(board, player):
    count = 0
    for i in range(24):
        if board[i] == player:
            if check_for_mill(board, player, i):
                count += 1

    return count
