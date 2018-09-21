from chess.state import GameState, Move
from chess.board import Board, Side
from mcst import UCT

if __name__ == '__main__':
    game_state = GameState()
    while game_state.winner() is None:
        if game_state.last_player() == Side.RED:
            m = UCT(rootstate = game_state, itermax = 1000, verbose=False)
        else:
            m = UCT(rootstate = game_state, itermax = 100, verbose=False)
        game_state.move(m)
        print(game_state.board)
    print("winner %s" % game_state.winner())
