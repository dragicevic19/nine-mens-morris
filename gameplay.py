import copy
import datetime
from alphabeta import *
from board import *
from evaluations import phase_23_relations
from tree import *

depth = 3
alpha = float('-inf')
beta = float('inf')


def maxscore(state, depth, alpha, beta, isPhase1):
    if not isPhase1:
        if winning_configuration(state.data, 'W', 'B') == 1:
            return float('inf')

    if depth <= 0:
        if isPhase1:
            return phase_one_relations(state.data, False)
        else:
            return phase_23_relations(state.data, False)

    for next_state in state.children:
        score = minscore(next_state, depth - 1, alpha, beta, isPhase1)
        alpha = max(alpha, score)
        if alpha >= beta:
            return beta

    return alpha


def minscore(state, depth, alpha, beta, isPhase1):
    if not isPhase1:
        if winning_configuration(state.data, 'B', 'W') == 1:
            return float('-inf')

    if depth <= 0:
        if isPhase1:
            return phase_one_relations(state.data, False)
        else:
            return phase_23_relations(state.data, False)

    for next_state in state.children:
        score = maxscore(next_state, depth - 1, alpha, beta, isPhase1)
        beta = min(beta, score)
        if alpha >= beta:
            return alpha

    return beta


MAX_POSSIBLE_SCORE = 1000


def next_move(root_board, depth, isPhase1):
    best_move = None
    alpha = float('-inf')
    for next_state in root_board.children:
        result = minscore(next_state, depth - 1, alpha, float('inf'), isPhase1)

        if result > alpha:
            alpha = result
            best_move = next_state.data
        if alpha >= MAX_POSSIBLE_SCORE:
            break
    return best_move


def game_phase1(board):
    print('========================= PHASE 1 =========================\n')
    for i in range(9):
        user_play_phase1(board)
        boardEval = alphabeta_pruning(board, depth, False, alpha, beta, True)
        board = boardEval.board
    return board
    #     stop1 = datetime.datetime.now()
    #     boards = bot_play_phase1(board, 'B')
    #     stop2 = datetime.datetime.now()
    #     board = next_move(boards, depth, True)
    #     stop3 = datetime.datetime.now()
    #     print('Pravi tablu: ', stop2 - stop1)
    #     print('Bira potez: ', stop3 - stop2)
    #     print('\nUkupno: ', stop3 - stop1)
    # return board


def user_play_phase1(board):
    print_board(board)
    correct = False
    while not correct:
        try:
            user_play = int(input('Izaberite polje >> '))
            correct = check_user_play(board, user_play)
        except ValueError:
            pass
    eat_if_possible(board, user_play)


def eat_if_possible(board, user_play):
    player = 'W'
    if check_for_mill(board, player, user_play):
        print_board(board)
        correct = False
        try:
            while not correct:
                remove_piece = int(input('Koju figuru zelite da pojedete? >> '))
                correct = check_for_removing_piece(board, remove_piece, player)
        except ValueError:
            pass


# #
# def bot_play_phase1(board, player):
#     tree_of_states = Tree()
#     tree_of_states.root = TreeNode(board)
#
#     make_a_tree(tree_of_states.root, depth, player)
#     return tree_of_states
#
#     # 11 156 tabli
#
#     # for state in tree_of_states.root.children:
#     #     # list_of_states.append(state.data)
#     #     for childState in state.children:
#     #         # list_of_states.append(childState.data)
#     #         for childchildState in childState.children:
#     #             list_of_states.append(childchildState.data)
#     #
#     # node_board = random.choice(tree_of_states.root.children)
#     #
#     # board = node_board.data
#
#
# def make_a_tree(root_board, depth, player):
#     if depth <= 0:
#         return
#
#     for i in range(24):
#         if root_board.data[i] == 'O':
#             copied_board = copy.deepcopy(root_board.data)
#             copied_board[i] = player
#             if check_for_mill(copied_board, player, i):
#                 for j in range(24):
#                     if copied_board[j] != 'O' and copied_board[j] != player:
#                         clone_for_removing = copy.deepcopy(copied_board)
#                         clone_for_removing = check_for_removing_piece(clone_for_removing, j, player)
#                         if clone_for_removing:
#                             node_clone = TreeNode(clone_for_removing)
#                             root_board.add_child(node_clone)
#
#                             if player == 'B':
#                                 make_a_tree(node_clone, depth - 1, player='W')
#                             else:
#                                 make_a_tree(node_clone, depth - 1, player='B')
#             else:
#                 node_clone = TreeNode(copied_board)
#                 root_board.add_child(node_clone)
#
#                 if player == 'B':
#                     make_a_tree(node_clone, depth - 1, player='W')
#                 else:
#                     make_a_tree(node_clone, depth - 1, player='B')


def game_phase2(board):
    print('========================= PHASE 2 =========================\n')
    while True:
        user_play_phase23(board)
        boardEval = alphabeta_pruning(board, depth, False, alpha, beta, False)
        if winning_configuration(boardEval.board, 'W', 'B') == -1:
            print('Izgubili ste!')
            exit(0)
        else:
            board = boardEval.board


def user_play_phase23(board):
    is_phase3 = is_phase_three(board, 'W')

    try:
        print_board(board)
    except IndexError:
        print('Izgubili ste!')
        exit(1)
    correct = False
    while not correct:
        try:
            user_play = input('Pomerite vasu figuru (x y) >> ')
            old, new = user_play.split(' ')
            old = int(old)
            new = int(new)
            correct = check_user_play_phase23(board, old, new, is_phase3, player='W')
        except ValueError:
            pass
    eat_if_possible(board, new)

    if winning_configuration(board, 'W', 'B') == 1:
        print('\nPobedili ste!')
        exit(0)


def is_phase_three(board, player):
    white_pieces, black_pieces = count_pieces(board, 'W', 'B')
    if player == 'W' and white_pieces == 3:
        return True
    if player == 'B' and black_pieces == 3:
        return True
    return False
