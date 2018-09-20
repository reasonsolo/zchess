# ref http://mcts.ai/code/python.html
from chess.board import Board

class Move:
    def __init__(self, piece, to):
        self.piece = piece
        self.piece_code = str(self.piece)
        self._from = (self.piece.x, self.piece.y)
        self._to = to

    def __str__(self):
        return "%s@%s>%s" % (self.piece_code, str(self._from), str(self._to))

class GameState:
    def __init__(self, board = Board()):
        self.board = board

    def clone(self):
        st = GameState()
        st.board = self.board.clone()
        return st

    def move(self, m):
        self.board.move(m.piece, *m._to)

    def all_moves(self):
        return [Move(p, m) for p, m in self.board.all_moves()]

    def last_player(self):
        return self.board.last_side()

    def winner(self):
        return self.board.winner()

    def last_player_is_winner(self, player):
        return last_player == self.winner()

    def __repr__(self):
        return self.board.state()
