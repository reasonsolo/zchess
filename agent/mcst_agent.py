from chess.state import GameState, Action
from collections import defaultdict

C_PUCT = 1.0

class McstNode:
    def __init__(self, state, parent=None, last_action=None):
        self.state = state
        self.parent = parent
        self.last_action = last_action

        self.n = 1
        self.w = 0
        self.prior_policy = {} # action -> prior policy
        self.children = {} # action -> node
        self.untried = set(self.state.all_actions)

    def get_prior_policy(self, action):
        return self.prior_policy[action] if len(self.prior_policy) == 0 else 1.0

    def select_child(self):
        def sort_key(a_c):
            a, c = a_c
            p = self.get_prior_policy(a)
            return c.w/c.n + C_PUCT*p*np.sqrt(c.n)/(c.n+1)
        return max(self.children.items(), key=sort_key)

    def select_action(self):
        def sort_key(a):
            return self.get_prior_policy(a)
        return max(self.untried, key=sort_key)

    def add_child(self, action, state):
        child = McstNode(state, self, action)
        self.untried.remove(action)
        self.children[action] = child

    def has_child(self, action):
        return action in self.children

    def update(self, result):
        self.w += result


class McstAgent:
    def __init__(self, side):
        self.side = side

    def select_move(self, state, n_sim=1000):
        root = McstNode(state)
        for _ in range(n_sim):
            node = root
            state = copy.deepcopy(state)
            while len(node.untried) == 0 and len(node.chilren) > 0:
                node = node.select_child()
                state.take_action(node.last_action)

            if len(node.untried) > 0:
                action = node.select_action()
                state.take_action(action)
                node = node.add_child(action, state)

            while len()


