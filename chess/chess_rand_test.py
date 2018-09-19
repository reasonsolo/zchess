from board import Board
import random


if __name__ == '__main__':
    b = Board()
    for i in range(0, 100):
        piece = random.choice(b.movable_pieces())
        try:
            move = random.choice(piece.possible_moves())
        except:
            print(piece, piece.x, piece.y)
        b.move(piece, *move)
        print(b)
        input(" ")
