from chess.state import GameState, Move
from chess.board import Board, Side
from mcst import UCT

if __name__ == '__main__':
    state = GameState()
    while state.winner() is None:
        if state.last_player() == Side.RED:
            m = UCT(rootstate = state, itermax = 1000, verbose=False)
        else:
            m = UCT(rootstate = state, itermax = 100, verbose=False)
        state.move(m)
        print(state.board)
    print("winner %s" % state.winner())
