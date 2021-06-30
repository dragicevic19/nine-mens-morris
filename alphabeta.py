from evaluations import *
from board import *
from tree import *


class Evaluator:

    def __init__(self):
        self.board = []
        self.evaluator = 0


def alphabeta_pruning(board, depth, player1, alpha, beta, is_stage1):
    final_evaluation = Evaluator()

    if depth != 0:
        current_evaluation = Evaluator()

        if player1:
            if is_stage1:
                possible_configs = bot_play_phase1(board, 'W')
            else:
                possible_configs = bot_play_phase23(board, 'W')
        else:
            if is_stage1:
                possible_configs = bot_play_phase1(board, 'B')
            else:
                possible_configs = bot_play_phase23(board, 'B')

        for move in possible_configs:
            if player1:
                current_evaluation = alphabeta_pruning(move.data, depth - 1, False, alpha, beta, is_stage1)

                if current_evaluation.evaluator > alpha:
                    alpha = current_evaluation.evaluator
                    final_evaluation.board = move.data
            else:
                current_evaluation = alphabeta_pruning(move.data, depth - 1, True, alpha, beta, is_stage1)

                if current_evaluation.evaluator < beta:
                    beta = current_evaluation.evaluator
                    final_evaluation.board = move.data

            if alpha >= beta:
                break

        if player1:
            final_evaluation.evaluator = alpha
        else:
            final_evaluation.evaluator = beta

    else:
        if player1:
            if is_stage1:
                final_evaluation.evaluator = phase_one_relations(board, True)
            else:
                final_evaluation.evaluator = phase_23_relations(board, True)
        else:
            if is_stage1:
                final_evaluation.evaluator = phase_one_relations(board, False)
            else:
                final_evaluation.evaluator = phase_23_relations(board, False)

    return final_evaluation


def bot_play_phase1(board, player):
    tree_of_states = Tree()
    tree_of_states.root = TreeNode(board)
    make_a_tree(tree_of_states.root, player)
    return tree_of_states.root.children  # vraca samo mogucnosti za jedan sledeci potez
    # testiraj(tree_of_states.root, player, depth=3)
    # return tree_of_states.root


def make_a_tree(root_board, player):
    for i in range(24):
        if root_board.data[i] == 'O':
            copied_board = copy.deepcopy(root_board.data)
            copied_board[i] = player
            if check_for_mill(copied_board, player, i):
                for j in range(24):
                    if copied_board[j] != 'O' and copied_board[j] != player:
                        clone_for_removing = copy.deepcopy(copied_board)
                        if check_for_removing_piece(clone_for_removing, j, player):
                            node_clone = TreeNode(clone_for_removing)
                            root_board.add_child(node_clone)
            else:
                node_clone = TreeNode(copied_board)
                root_board.add_child(node_clone)


def testiraj(cvor, player, depth):
    if depth > 0:
        if player == 'W':
            player2 = 'B'
        else:
            player2 = 'W'
        make_a_tree(cvor, player)
        for i in cvor.children:
            testiraj(i, player2, depth - 1)


#
# # def racunajheuristikuZaList(root):
#     for child in root.children:


def bot_play_phase23(board, player):
    from gameplay import is_phase_three
    tree_of_states = Tree()
    tree_of_states.root = TreeNode(board)
    is_phase3 = is_phase_three(board, player)
    make_a_tree_phase23(tree_of_states.root, player, is_phase3)

    return tree_of_states.root.children


def make_a_tree_phase23(root_board, player, is_phase3):
    for old in range(24):
        if root_board.data[old] == player:
            copied_board = copy.deepcopy(root_board.data)

            if is_phase3:
                phase3_move(copied_board, is_phase3, old, player, root_board)

            else:
                phase2_move(copied_board, is_phase3, old, player, root_board)


def phase2_move(copied_board, is_phase3, old, player, root_board):
    for new in nearby_places(old):
        if check_user_play_phase23(copied_board, old, new, is_phase3, player):

            if check_for_mill(copied_board, player, new):
                removing_piece(copied_board, player, root_board)
            else:
                root_board.add_child(TreeNode(copied_board))


def phase3_move(copied_board, is_phase3, old, player, root_board):
    for new in range(24):
        if check_user_play_phase23(copied_board, old, new, is_phase3, player):

            if check_for_mill(copied_board, player, new):
                removing_piece(copied_board, player, root_board)
            else:
                root_board.add_child(TreeNode(copied_board))


def removing_piece(copied_board, player, root_board):
    for remove in range(24):
        if copied_board[remove] != player and copied_board[remove] != 'O':
            clone_for_removing = copy.deepcopy(copied_board)

            if check_for_removing_piece(clone_for_removing, remove, player):
                root_board.add_child(TreeNode(clone_for_removing))

            else:
                root_board.add_child(TreeNode(copied_board))
