import copy
import random


class TreeNode(object):
    __slots__ = 'parent', 'children', 'data'

    def __init__(self, data):
        self.parent = None
        self.children = []
        self.data = data

    def add_child(self, x):
        x.parent = self
        self.children.append(x)


class Tree(object):
    def __init__(self):
        self.root = None


class MapElement(object):
    __slots__ = '_key', '_value'

    def __init__(self, key, value):
        self._key = key
        self._value = value

    def get_key(self):
        return self._key

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self._value = new_value


class HashMap(object):
    def __init__(self, capacity=8):

        self._data = capacity * [None]
        self._capacity = capacity
        self._size = 0
        self.prime = 109345121

        self._a = 1 + random.randrange(self.prime - 1)
        self._b = random.randrange(self.prime)

    def __len__(self):
        return self._size

    def _hash(self, x):
        hashed_value = (hash(x) * self._a + self._b) % self.prime
        compressed = hashed_value % self._capacity
        return compressed

    def _resize(self, capacity):

        old_data = list(self.items())
        self._data = capacity * [None]
        self._size = 0
        for (k, v) in old_data:
            self[k] = v

    def __getitem__(self, key):

        bucket_index = self._hash(key)
        return self._bucket_getitem(bucket_index, key)

    def __setitem__(self, key, value):
        bucket_index = self._hash(key)
        self._bucket_setitem(bucket_index, key, value)

        current_capacity = len(self._data)
        if self._size > current_capacity // 2:
            self._resize(2 * current_capacity - 1)

    def __delitem__(self, key):
        bucket_index = self._hash(key)
        self._bucket_delitem(bucket_index, key)
        self._size -= 1


class LinearHashMap(HashMap):
    _MARKER = object()

    def _is_available(self, i):
        return self._data[i] is None or self._data[i] is self._MARKER

    def _find_bucket(self, i, key):
        available_slot = None
        while True:
            if self._is_available(i):
                if available_slot is None:
                    available_slot = i

                if self._data[i] is None:
                    return (False, available_slot)
            elif key == self._data[i].get_key():
                return (True, i)

            i = (i + 1) % len(self._data)

    def _bucket_getitem(self, i, key):

        found, index = self._find_bucket(i, key)
        if not found:
            raise KeyError('Ne postoji element sa traženim ključem.')
        return self._data[index].get_value()

    def _bucket_setitem(self, i, key, value):

        found, index = self._find_bucket(i, key)
        if not found:
            self._data[index] = MapElement(key, value)
            self._size += 1
        else:
            self._data[index].set_value(value)

    def _bucket_delitem(self, i, key):

        found, index = self._find_bucket(i, key)
        if not found:
            raise KeyError('Ne postoji element sa traženim ključem.')

        self._data[index] = self._MARKER

    def __iter__(self):
        total_buckets = len(self._data)
        for i in range(total_buckets):
            if not self._is_available(i):
                yield self._data[i].get_key()


def find_coordinates(input_board, end_board, isInit, isMill):
    dict = {
        0: '0 0',
        1: '0 3',
        2: '0 6',
        3: '1 1',
        4: '1 3',
        5: '1 5',
        6: '2 2',
        7: '2 3',
        8: '2 4',
        9: '3 0',
        10: '3 1',
        11: '3 2',
        12: '3 4',
        13: '3 5',
        14: '3 6',
        15: '4 2',
        16: '4 3',
        17: '4 4',
        18: '5 1',
        19: '5 3',
        20: '5 5',
        21: '6 0',
        22: '6 3',
        23: '6 6'
    }
    first_coordinate = []
    second_coordinate = []
    for i in range(24):
        if input_board[i] != end_board[i]:
            if input_board[i] == 'W' or input_board[i] == 'B':
                first_coordinate = dict[i].split(' ')
            else:
                second_coordinate = dict[i].split(' ')
            if isInit or isMill:
                break
            if first_coordinate and second_coordinate:
                break
    if isInit:
        return second_coordinate
    elif isMill:
        return first_coordinate
    else:
        return first_coordinate, second_coordinate


def nextMove(player, move, board):
    alpha = float('-inf')
    beta = float('inf')
    depth = 3
    input_board = LinearHashMap(50)
    input_board = make_board(board, input_board)
    # input_board = make_board_test(board, input_board)

    isPlayer1 = False
    if player == 'W':
        isPlayer1 = True

    if move == 'INIT':
        boardEval = alphabeta_pruning(input_board, depth, isPlayer1, alpha, beta, True, isMill=False)
        board = boardEval.board
        coordinates = find_coordinates(input_board, board, True, False)
        print('{} {}'.format(int(coordinates[0]), int(coordinates[1])))

    if move == 'MOVE':
        boardEval = alphabeta_pruning(input_board, depth, isPlayer1, alpha, beta, False, isMill=False)
        board = boardEval.board
        coordinates1, coordinates2 = find_coordinates(input_board, board, False, False)
        print('{} {} {} {}'.format(int(coordinates1[0]), int(coordinates1[1]), int(coordinates2[0]),
                                   int(coordinates2[1])))

    if move == 'MILL':
        boardEval = alphabeta_pruning(input_board, depth, isPlayer1, alpha, beta, True, isMill=True)
        board = boardEval.board
        coordinates = find_coordinates(input_board, board, False, True)
        print('{} {}'.format(int(coordinates[0]), int(coordinates[1])))


def print_board(board):
    print(board[0] + "--" + board[1] + "--" + board[2])
    print('|' + board[3] + '-' + board[4] + '-' + board[5] + '|')
    print('||' + board[6] + board[7] + board[8] + '||')
    print(board[9] + board[10] + board[11] + '*' + board[12] + board[13] + board[14])
    print('||' + board[15] + board[16] + board[17] + '||')
    print('|' + board[18] + '-' + board[19] + '-' + board[20] + '|')
    print(board[21] + "--" + board[22] + "--" + board[23])


def nearby_places(user_play):
    nearby_locations = [
        [1, 9],
        [0, 2, 4],
        [1, 14],
        [10, 4],
        [3, 5, 1, 7],
        [4, 13],
        [11, 7],
        [4, 6, 8],
        [7, 12],
        [0, 21, 10],
        [9, 3, 18, 11],
        [6, 15, 10],
        [8, 17, 13],
        [12, 5, 20, 14],
        [13, 2, 23],
        [11, 16],
        [17, 15, 19],
        [16, 12],
        [10, 19],
        [18, 20, 16, 22],
        [19, 13],
        [9, 22],
        [21, 19, 23],
        [22, 14]
    ]
    return nearby_locations[user_play]


def check_for_mill(board, player_color, user_play):
    mill = [
        [[1, 2], [9, 21]],
        [[0, 2], [4, 7]],
        [[0, 1], [14, 23]],
        [[10, 18], [4, 5]],
        [[1, 7], [3, 5]],
        [[3, 4], [13, 20]],
        [[11, 15], [7, 8]],
        [[4, 1], [6, 8]],
        [[6, 7], [12, 17]],
        [[0, 21], [10, 11]],
        [[9, 11], [3, 18]],
        [[9, 10], [6, 15]],
        [[8, 17], [13, 14]],
        [[12, 14], [5, 20]],
        [[12, 13], [2, 23]],
        [[6, 11], [16, 17]],
        [[15, 17], [19, 22]],
        [[15, 16], [8, 12]],
        [[3, 10], [19, 20]],
        [[18, 20], [16, 22]],
        [[18, 19], [5, 13]],
        [[0, 9], [22, 23]],
        [[21, 23], [16, 19]],
        [[2, 14], [21, 22]],
    ]
    player_pieces = 0
    mills = 0
    nearby_locations = mill[user_play]
    for list_of_locations in nearby_locations:
        player_pieces = 0
        for location in list_of_locations:
            if board[location] == player_color:
                player_pieces += 1
        if player_pieces == 2:
            return True

    return False


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


def make_board(board, board_map):
    i = 0
    for list in board:
        for char in list:
            if char == 'O' or char == 'W' or char == 'B':
                board_map[i] = char
                i += 1
    return board_map


class Evaluator:

    def __init__(self):
        self.board = []
        self.evaluator = 0


def bot_eat(board, player):
    tree = Tree()
    tree.root = TreeNode(board)
    for remove in range(24):
        if board[remove] != player and board[remove] != 'O':
            clone_for_removing = copy.deepcopy(board)
            if check_for_removing_piece(clone_for_removing, remove, player):
                tree.root.add_child(TreeNode(clone_for_removing))

    return tree.root.children


def alphabeta_pruning(board, depth, player1, alpha, beta, is_stage1, isMill):
    final_evaluation = Evaluator()

    if depth != 0:
        current_evaluation = Evaluator()

        if player1:
            if is_stage1:
                if isMill:
                    possible_configs = bot_eat(board, 'W')
                else:
                    possible_configs = bot_play_phase1(board, 'W')

            else:
                if isMill:
                    possible_configs = bot_eat(board, 'W')
                else:
                    possible_configs = bot_play_phase23(board, 'W')

        else:
            if is_stage1:
                if isMill:
                    possible_configs = bot_eat(board, 'B')
                else:
                    possible_configs = bot_play_phase1(board, 'B')
            else:
                if isMill:
                    possible_configs = bot_eat(board, 'B')
                else:
                    possible_configs = bot_play_phase23(board, 'B')

        for move in possible_configs:
            if player1:
                current_evaluation = alphabeta_pruning(move.data, depth - 1, False, alpha, beta, is_stage1, False)

                if current_evaluation.evaluator > alpha:
                    alpha = current_evaluation.evaluator
                    final_evaluation.board = move.data
            else:
                current_evaluation = alphabeta_pruning(move.data, depth - 1, True, alpha, beta, is_stage1, False)

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


def make_a_tree(root_board, player):
    for i in range(24):
        if root_board.data[i] == 'O':
            copied_board = copy.deepcopy(root_board.data)
            copied_board[i] = player
            # if check_for_mill(copied_board, player, i):
            #     for j in range(24):
            #         if copied_board[j] != 'O' and copied_board[j] != player:
            #             clone_for_removing = copy.deepcopy(copied_board)
            #             check_for_removing_piece(clone_for_removing, j, player)
            #             node_clone = TreeNode(clone_for_removing)
            #             root_board.add_child(node_clone)
            # else:
            node_clone = TreeNode(copied_board)
            root_board.add_child(node_clone)


def bot_play_phase23(board, player):
    tree_of_states = Tree()
    tree_of_states.root = TreeNode(board)
    is_phase3 = is_phase_three(board, player)
    make_a_tree_phase23(tree_of_states.root, player, is_phase3)

    return tree_of_states.root.children


def is_phase_three(board, player):
    white_pieces, black_pieces = count_pieces(board, 'W', 'B')
    if player == 'W' and white_pieces == 3:
        return True
    if player == 'B' and black_pieces == 3:
        return True
    return False


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
            root_board.add_child(TreeNode(copied_board))

            # if check_for_mill(copied_board, player, new):
            #     removing_piece(copied_board, player, root_board)
            # else:
            #     root_board.add_child(TreeNode(copied_board))


def phase3_move(copied_board, is_phase3, old, player, root_board):
    for new in range(24):
        if check_user_play_phase23(copied_board, old, new, is_phase3, player):
            root_board.add_child(TreeNode(copied_board))

            # if check_for_mill(copied_board, player, new):
            #     removing_piece(copied_board, player, root_board)
            # else:
            #     root_board.add_child(TreeNode(copied_board))


def removing_piece(copied_board, player, root_board):
    for remove in range(24):
        if copied_board[remove] != player and copied_board[remove] != 'O':
            clone_for_removing = copy.deepcopy(copied_board)

            if check_for_removing_piece(clone_for_removing, remove, player):
                root_board.add_child(TreeNode(clone_for_removing))

            else:
                root_board.add_child(TreeNode(copied_board))


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
    if check_for_mill(board, player, i):  # mozda moze efikasnije??
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
    evaluation += 43 * num_of_morrises(board, player1, player2)
    evaluation += 10 * num_of_blocked_opp_pieces(board, player1, player2)
    evaluation += 11 * num_of_pieces(board, player1, player2)
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
    # evaluation += 43 * num_of_morrises(board, player1, player2)
    evaluation += 10 * num_of_2_pieces(board, player1, player2)
    evaluation += 1 * num_of_3_pieces(board, player1, player2)
    evaluation += 1190 * winning_configuration(board, player1, player2)
    return evaluation


player = input().strip()
move = input().strip()
board = []
for i in range(7):
    board.append(input().strip())

nextMove(player, move, board)
