# ref http://mcts.ai/code/python.html
from chess.board import Board
import itertools

class InvalidActionError(Exception):
    pass

class Action:
    def __init__(self, piece, to):
        self.piece = piece
        self.piece_code = str(self.piece)
        self._from = (self.piece.x, self.piece.y)
        self._to = to

    def __str__(self):
        return "%s@%s>%s" % (self.piece_code, str(self._from), str(self._to))

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.piece_code == other.piece_code and self._from == other._from and self._to == other._to


class GameState:
    def __init__(self, players, init=True, board=None):
        if init:
            self.board = Board()
        else:
            self.board = board
        self.end = False
        self.winner = None
        self.current_player = players[0]
        self.players = itertools.cycle(players)
        self.all_actions = [Action(piece, move) for piece, move in self.board.all_moves()]
        self.history = []

    def take_action(self, action):
        action_str = str(action)
        if action_str not in self.all_actions:
            raise InvalidActionError
        self.history.append(action)
        self.board.move(action.piece, *action.to)
        self.update()

    def update(self):
        self.winner = self.board.winner()
        self.end = True if winner is not None or self.board.draw() else False
        self.current_player = next(self.players)
        self.all_actions = [Action(piece, move) for piece, move in self.board.all_moves()]

    def repeat_times(self):
        # TODO
        pass

    def __repr__(self):
        return self.board.state()
