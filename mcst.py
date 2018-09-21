from math import sqrt, log
import random


class Node:
    def __init__(self, move = None, parent = None, state = None):
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = {str(move): move for move in state.all_moves()}
        self.last_player = state.last_player()

    def uct_select_child(self):
        s = sorted(self.children, key = lambda c: c.wins / c.visits\
                   + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def add_child(self, m, s):
        n = Node(move=m, parent=self, state=s)
        del self.untried_moves[str(m)]
        self.children.append(n)

    def update(self, win):
        self.visits += 1
        self.wins += int(win)

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/"\
            + str(self.visits) + " U:" + str(self.untried_moves) + "]"


# FIXME: buggy
def UCT(rootstate, itermax, verbose=False):
    root = Node(state=rootstate)
    for i in range(itermax):
        node = root
        state = rootstate.clone()
        print(state)
        # select
        # fully expanded but non-terminal
        while len(node.untried_moves) == 0 and len(node.children) > 0:
            node = node.uct_select_child()
            state.move(node.move)

        # expand
        if len(node.untried_moves) > 0:
            m = random.choice(list(node.untried_moves.values()))
            state.move(m)
            node = node.add_child(m, state)

        # rollout
        while len(state.all_moves()) > 0:
            state.move(random.choice(state.all_moves()))

        # backpropagate
        while node != None:
            node.update(state.last_player_is_winner())
            node = node.parent
        print(state)

    return sorted(root.children, key = lambda c: c.visits)[-1].move







