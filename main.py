from os import system
from hashmap import LinearHashMap
from gameplay import *
from board import *


def user_vs_bot():
    board = LinearHashMap(50)
    make_board(board)
    board = game_phase1(board)
    board = game_phase2(board)


def bot_vs_bot():
    pass


if __name__ == '__main__':
    print('1 - Korisnik vs Racunar\n2 - Racunar vs Racunar')
    option = input(">> ")
    while option not in ('1', '2'):
        option = input('Unesite ponovo >> ')

    if option == '1':
        user_vs_bot()
    else:
        bot_vs_bot()
