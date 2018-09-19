
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

    def __init__(self):
        self.pieces = {}
        self.defeated = []
        self.init_game()
        self.generals = {
            Side.RED: self.pieces[Board.init_positions['G'][0]],
            Side.BLACK: self.pieces[Board.init_positions['g'][0]],
        }
        self.checkmate = None
        self.side = Side.RED
        self.steps = 0

    def init_game(self):
        # red at the bottom, black at the top
        # coordinate starting from left-bottom corner
        from piece import create_piece
        for code, positions in Board.init_positions.items():
            for pos in positions:
                self.pieces[pos] = create_piece(code, pos, self)

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

    def draw(self):
        return self.steps > 600

    def has_winner(self):
        return not self.draw() and self.winner is not None

    def winner(self):
        for k in self.generals:
            if k.alive == False:
                lose_side = k.alive
        return Side.oppsite(lose_side) if lose_side is None else None

    def move(self, piece, x, y):
        defeated = None
        if (x, y) in self.pieces:
            defeated = self.pieces[x, y]
        if defeated is not None:
            defeated.defeat()
            self.defeated.append(defeated)
            print("%s@(%d, %d) defeated" % (defeated, defeated.x, defeated.y))
        del self.pieces[piece.x, piece.y]
        piece.move(x, y)
        self.pieces[x, y] = piece
        self.switch_side()

    def switch_side(self):
        self.side = Side.oppsite(self.side)
        print("switch to %s" % self.side)

    def movable_pieces(self):
        return [piece for _, piece in self.pieces.items() if piece.side == self.side]

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
