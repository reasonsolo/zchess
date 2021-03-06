from board import Board
import random
import copy

if __name__ == '__main__':
    b = Board()
    b2 = b.clone()
    for i in range(0, 1000):
        if b.has_winner():
            print("winner is ", b.winner())
            break
        piece = random.choice(b.movable_pieces())
        moves = piece.possible_moves()
        if len(moves) == 0:
            print(piece, " not movable")
            continue
        move = random.choice(moves)
        b.move(piece, *move)
        print(b)
        print(b.state())
        print(b2.state())
        input(" ")
