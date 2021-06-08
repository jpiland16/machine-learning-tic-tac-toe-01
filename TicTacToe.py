"""
A note: the board has the following layout:

 0 | 1 | 2
---|---|---
 3 | 4 | 5
---|---|---
 6 | 7 | 8 

"""

WINNING_COMBOS = (
    [[0, 1, 2], 
     [0, 4, 8],
     [0, 3, 6],
     [1, 4, 7],
     [2, 5, 8],
     [2, 4, 6],
     [3, 4, 5],
     [6, 7, 8]]
)

class Move():
    """
    A move in the game. Stores position and player.
    """        
    def __init__(self, pos: int, player: int) -> None:
        self.pos = pos
        self.player = player

class GameState():
    """
    A state of the game of Tic-Tac-Toe. 
    Player X (represented as 1) goes first.
    Player O (represented as -1) goes second.
    """
    def __init__(self, board=[0, 0, 0, 0, 0, 0, 0, 0, 0]) -> None:
        self.board = board
        self.next_player = 1

    def get_valid_moves(self) -> 'list[Move]':
        valid_moves = []
        for pos, value in enumerate(self.board):
            if value == 0:
                valid_moves.append(Move(pos, self.next_player))
        return valid_moves
    
    def is_move_valid(self, move: Move) -> bool:
        return self.board[move.pos] == 0

    def to_integer(self) -> int:
        integer_representation = 0
        for pos, value  in enumerate(self.board):
            integer_representation += (value + 1) * (3 ** pos) 
        return int(integer_representation)

    def move(self, move: Move) -> None:
        self.board[move.pos] = move.player
        self.next_player *= -1

    def get_winner(self):
        """
        Returns -1 if O has won, 1 if X has won, or 0 if nobody has won.
        """
        for combo in WINNING_COMBOS:
            if self.board[combo[0]] != 0 and \
                self.board[combo[0]] == self.board[combo[1]] and \
                self.board[combo[1]] == self.board[combo[2]]:
                    return self.board[combo[0]]
        return 0

    def whose_turn(self) -> int:
        # X - O: 
        diff = sum([v for v in self.board])
        if diff == 0:
            return 1
        if diff == 1:
            return -1
        return 0 # error

    def __str__(self):
        return ("\n"
                " {0} | {1} | {2} \n" +
                "-----|-----|-----\n" +
                " {3} | {4} | {5} \n" +
                "-----|-----|-----\n" +
                " {6} | {7} | {8} \n\n[{9}]\n").format(
                    *[["(O)", "   ", "[X]"][i + 1] for i in self.board], 
                    self.to_integer() 
                )

def get_game_after_move(now: GameState, move: Move) -> GameState:
    then = GameState(now.board.copy())
    then.move(move)
    return then

def is_valid_state(game: GameState) -> bool:
    x_count = 0
    o_count = 0
    for value in game.board:
        if value == -1:
            o_count += 1
        elif value == 1:
            x_count += 1
    diff = x_count - o_count
    if diff == 0 or diff == 1:
        x_wins = []
        o_wins = []
        for combo in WINNING_COMBOS:
            if game.board[combo[0]] != 0 and \
                game.board[combo[0]] == game.board[combo[1]] and \
                game.board[combo[1]] == game.board[combo[2]]:
                    if game.board[combo[0]] == 1:
                        x_wins.append(combo)
                    if game.board[combo[0]] == -1:
                        o_wins.append(combo)
        if len(x_wins) + len(o_wins) <= 1:
            if len(o_wins) == 1:
                if diff == 0:
                    return True
            elif len(x_wins) == 1:
                if diff == 1:
                    return True
            else:
                return True
        elif len(x_wins) == 2:
            if lines_intersect(x_wins[0], x_wins[1]):
                return True
    return False

def lines_intersect(l1: 'list[int]', l2: 'list[int]'):
    for cell1 in l1:
        for cell2 in l2:
            if cell1 == cell2:
                return True
    return False


def get_game_from_int(n: int) -> GameState:
    board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range (0, 9):
        r = n % 3
        board[i] = r - 1
        n -= r
        n //= 3
    return GameState(board=board)