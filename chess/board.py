# -*- coding: utf-8 -*-
import copy

class InvalidMoveError(Exception):
    pass

class InvalidBoardError(Exception):
    pass

class Side:
    RED = 1
    BLACK = 2
    def oppsite(side):
        return Side.BLACK if side == Side.RED else Side.RED

class Board:
    width = 9
    height = 10

    init_positions = {
        # red
        'R': [(0, 0), (8, 0)],
        'H': [(1, 0), (7, 0)],
        'E': [(2, 0), (6, 0)],
        'A': [(3, 0), (5, 0)],
        'G': [(4, 0)],
        'C': [(1, 2), (7, 2)],
        'S': [(0, 3), (2, 3), (4, 3), (6, 3), (8, 3)],
        # black
        'r': [(0, 9), (8, 9)],
        'h': [(1, 9), (7, 9)],
        'e': [(2, 9), (6, 9)],
        'a': [(3, 9), (5, 9)],
        'g': [(4, 9)],
        'c': [(1, 7), (7, 7)],
        's': [(0, 6), (2, 6), (4, 6), (6, 6), (8, 6)]
    }
    id = 0
    def __init__(self, init=True):
        self.pieces = {}
        self.defeated = []
        self.generals = {}
        self.checkmate = None
        self.side = Side.RED
        self.steps = 0
        if init:
            self.init_game()

    def clone(self):
        b = Board(init=False)
        from chess.piece import General
        for (x, y), p in self.pieces.items():
            piece = p.__class__(p.side, (p.x, p.y), b)
            b.pieces[x, y] = piece
            if isinstance(p, General):
                b.generals[piece.side] = piece
        for p in self.defeated:
            piece = p.__class__(p.side, (p.x, p.y), b)
            piece.alive = False
            b.defeated.append(piece)
        print("cpy %s\n to %s" % (self.state(), b.state()))
        b.checkmate = self.checkmate
        b.side = self.side
        b.steps = self.steps
        return b

    def __deepcopy__(self, memo):
        return self.clone()

    def init_game(self):
        # red at the bottom, black at the top
        # coordinate starting from left-bottom corner
        from chess.piece import create_piece
        for code, positions in Board.init_positions.items():
            for pos in positions:
                self.pieces[pos] = create_piece(code, pos, self)
        self.generals = {
            Side.RED: self.pieces[Board.init_positions['G'][0]],
            Side.BLACK: self.pieces[Board.init_positions['g'][0]],
        }

    def can_move(self, piece, x, y):
        if x == piece.x and y == piece.y:
            return False
        if (x, y) in self.pieces:
            target_pieces = self.pieces[x, y]
            return target_pieces.side != piece.side
        else:
            return x in range(0, Board.width) and y in range(0, Board.height)

    def piece_at(self, x, y):
        if (x, y) in self.pieces:
            return self.pieces[x, y]
        return None

    def checkmate(self):
        """
        the other side must respond to checkmate by rule
        """
        pass

    def last_side(self):
        return Side.oppsite(self.side)

    def cur_side(self):
        return self.side

    # FIXME: cannot draw
    def draw(self):
        return self.steps > 600

    def has_winner(self):
        return self.winner() is not None

    def winner(self):
        lose_side = None
        for i, g in self.generals.items():
            if g.alive == False:
                lose_side = g.side

        if lose_side is None:
            for side in (Side.RED, Side.BLACK):
                if len(self.movable_pieces(side)) == 0:
                    lose_side = side
        return Side.oppsite(lose_side) if lose_side is not None else None

    def move(self, piece, x, y):
        defeated = None
        if self.side != piece.side:
            raise InvalidMoveError
        if (x, y) in self.pieces:
            defeated = self.pieces[x, y]
            defeated.defeat()
            self.defeated.append(defeated)
            del self.pieces[x, y]
        del self.pieces[piece.x, piece.y]
        piece.move(x, y)
        self.pieces[x, y] = piece
        self.switch_side()
        self.steps += 1
        # print("move %s" % self.state())

    def switch_side(self):
        self.side = Side.oppsite(self.side)

    def movable_pieces(self, side = None):
        if side == None:
            side = self.side
        return [piece for piece in self.pieces.values() if piece.side == side and len(piece.possible_moves()) > 0]

    def all_moves(self, side = None):
        if self.has_winner():
            return []
        if side == None:
            side = self.side
        return [(piece, move) for piece in self.pieces.values() if piece.side == side for move in piece.possible_moves()]

    def state(self):
        state_str = str(self.side) + "|" + str(self.steps) + "|"
        for y in range(0, Board.height):
            for x in range(0, Board.width):
                if (x, y) not in self.pieces:
                    state_str += "_"
                else:
                    state_str += str(self.pieces[x, y])
                    # piece = self.pieces[x, y]
                    # if (piece.x, piece.y) != (x, y):
                    #     print("invalid piece state")
        return state_str

    def piece_check(self):
        for (x, y), p in self.pieces.items():
            if (x, y) != (p.x, p.y):
                print("invalid state %s (%d, %d) (%d, %d)" % (piece, piece.x, piece.y, x, y))
                raise InvalidBoardError

    def __repr__(self):
        ret = "Board\n"
        for y in reversed(range(0, Board.height)):
            for x in range(0, Board.width):
                if (x, y) not in self.pieces:
                    ret += "十"
                else:
                    ret += repr(self.pieces[x, y])
            ret += "\n"
        return ret
