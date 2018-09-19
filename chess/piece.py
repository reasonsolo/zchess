# -*- coding: utf-8 -*-
from state import GameState
from board import Side, Board

class InvalidPieceError(Exception):
    pass


class Piece:
    def __init__(self, side, position, board = None):
        self.side = side
        self.board = board
        self.alive = True
        self.x, self.y = position

    def move(self, x, y):
        self.x, self.y = x, y

    def all_moves(self):
        raise NotImplementedError

    def possible_moves(self):
        return [move for move in self.all_moves() if self.board.can_move(self, *move) and self.can_move(*move)]

    def checkmate(self):
        raise NotImplementedError

    def can_move(self, x, y):
        raise NotImplementedError

    def defeat(self):
        self.alive = False

    def add_to_board(self, board, x, y):
        self.board = board
        self.x = x
        self.y = y

    def __repr__(self):
        raise NotImplementedError


class General(Piece):
    def can_move(self, x, y):
        if self.side == Side.RED:
            if x not in range(3, 6) or y not in range(0, 3):
                return False
            # kings can't meet in a line
            for i in range(self.y + 1, Board.height):
                piece = self.board.piece_at(x, i)
                if piece is not None:
                    if piece.side != self.side and isinstance(piece, General):
                        return False
                    else:
                        return True
                    break
        else:
            if x not in range(3, 6) or y not in range(7, 10):
                return False
            for i in reversed(range(0, self.y)):
                piece = self.board.piece_at(x, i)
                if piece is not None:
                    if piece.side != self.side and isinstance(piece, General):
                        return False
                    else:
                        return True
                    break
        return True

    def all_moves(self):
        x, y = self.x, self.y
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

    def __repr__(self):
        return "帥" if self.side == Side.RED else "將"


class Advisor(Piece):
    def all_moves(self):
        x, y = self.x, self.y
        return [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]

    def can_move(self, x, y):
        if self.side == Side.RED:
            if x not in range(3, 6) or y not in range(0, 3):
                return False
        else:
            if x not in range(3, 6) or y not in range(7, 10):
                return False
        return True

    def __repr__(self):
        return "仕" if self.side == Side.RED else "士"


class Elephant(Piece):
    def all_moves(self):
        x, y = self.x, self.y
        return [(x+2, y+2), (x+2, y-2), (x-2, y+2), (x-2, y-2)]

    def can_move(self, x, y):
        hole = (self.x+x)/2, (self.y+y)/2
        if self.board.piece_at(hole) is not None:
            return False
        if self.side == Side.RED:
            return y in range(0, 5)
        else:
            return y in range(6, 10)

    def __repr__(self):
        return "相" if self.side == Side.RED else "象"


class Horse(Piece):
    def all_moves(self):
        x, y = self.x, self.y
        return [(x+1, y+2), (x+1, y-2), (x+2, y+1), (x+2, y-1),
                (x-1, y+2), (x-1, y-2), (x-2, y+1), (x-2, y-1)]

    def can_move(self, x, y):
        dx, dy = x - self.x, y - self.y
        hole = self.x, self.y
        if abs(dx) == 2:
            hole = (self.x+x)/2, self.y
        elif abs(dy) == 2:
            hole = self.x, (self.y+y)/2
        else:
            raise InvalidPieceError
        return self.board.piece_at(*hole) is None

    def __repr__(self):
        return "傌" if self.side == Side.RED else "馬"


class Rook(Piece):
    def all_moves(self):
        return [(x, self.y) for x in range(0, Board.width)] + [(self.x, y) for y in range(0, Board.height)]

    def can_move(self, x, y):
        if self.x == x:
            for e, i in enumerate(range(self.y, y, -1 if self.y > y else 1)):
                if e == 0:
                    continue
                if self.board.piece_at(self.x, i) is not None:
                    return False
        if self.y == y:
            for e, i in enumerate(range(self.x, x, -1 if self.x > x else 1)):
                if e == 0:
                    continue
                if self.board.piece_at(i, self.y) is not None:
                    return False
        return True

    def __repr__(self):
        return "俥" if self.side == Side.RED else "車"


class Cannon(Piece):
    def all_moves(self):
        return [(x, self.y) for x in range(0, Board.width)] + [(self.x, y) for y in range(0, Board.height)]

    def can_move(self, x, y):
        if self.board.piece_at(x, y) is None:
            if self.x == x:
                for e, i in enumerate(range(self.y, y, -1 if self.y > y else 1)):
                    if e == 0:
                        continue
                    if self.board.piece_at(self.x, i) is not None:
                        return False
            if self.y == y:
                for e, i in enumerate(range(self.x, x, -1 if self.x > x else 1)):
                    if e == 0:
                        continue
                    if self.board.piece_at(i, self.y) is not None:
                        return False
        else:
            has_pivot = 0
            if self.x == x:
                for e, i in enumerate(range(self.y, y, -1 if self.y > y else 1)):
                    if e == 0:
                        continue
                    if not has_pivot and self.board.piece_at(self.x, i) is not None:
                        has_pivot = True
                    elif self.board.piece_at(self.x, i) is not None:
                        return False
            if self.y == y:
                for e, i in enumerate(range(self.x, x, -1 if self.x > x else 1)):
                    if e == 0:
                        continue
                    if not has_pivot and self.board.piece_at(i, self.y) is not None:
                        has_pivot = True
                    elif self.board.piece_at(i, self.y) is not None:
                        return False
        return True


    def __repr__(self):
        return "炮" if self.side == Side.RED else "砲"


class Soldier(Piece):
    def all_moves(self):
        x, y = self.x, self.y
        if self.side == Side.RED:
            return [(x+1, y), (x, y+1), (x-1, y)] if self.y > 4 else [(x, y+1)]
        else :
            return [(x+1, y), (x, y-1), (x-1, y)] if self.y < 5 else [(x, y-1)]

    def can_move(self, x, y):
        return True

    def __repr__(self):
        return "兵" if self.side == Side.RED else "卒"


PIECE_CODES = {
    'G': General,
    'A': Advisor,
    'E': Elephant,
    'H': Horse,
    'R': Rook,
    'C': Cannon,
    'S': Soldier,
}


def create_piece(code, position, board):
    side = Side.RED if code.isupper() else Side.BLACK
    code = code.upper()
    if code not in PIECE_CODES:
        raise InvalidPieceError
    return PIECE_CODES[code](side, position, board)


