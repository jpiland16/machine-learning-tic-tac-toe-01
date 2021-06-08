from AI import get_ai_move
from TicTacToe import GameState, get_game_from_int
from Interface import confirm, cool_type,  spin, set_enable_animations, get_valid_human_move
from Files import get_latest_ai_version, get_pickle
import random, sys
import getopt

USAGE = "usage: -b <board_id> -p <player_id> -v <ai_version>\n" + \
        "flags: -h (help) -f (disable animations) -d (dev) -m (master dev)"

dev = False
master = False

def main():
    global state_values, dev, master

    board_start = None
    player_start = None
    ai_version = -1
    enable_animations = 1

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hb:p:v:fdm",
            ["help", "board=", "player-id=", "ai-version=", "fast", "dev",
            "master"])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(USAGE)
            elif opt in ("-b", "--board"):
                board_start = get_game_from_int(int(arg)).board
            elif opt in ("-p", "--player-id"):
                player_start = int(arg)
            elif opt in ("-v", "--ai-version"):
                ai_version = int(arg)
            elif opt in ("-f", "--fast"):
                enable_animations = 0
            elif opt in ("-d", "--dev"):
                dev = True
            elif opt in ("-m", "--master"):
                dev = True
                master = True

    except getopt.GetoptError as e:
        print(e)
        print(USAGE)
    
    set_enable_animations(enable_animations)
    state_values = get_pickle(ask_confirm=False, use_version=ai_version)

    if state_values == None:
        print("Pickle could not be loaded.")
        sys.exit()

    cool_type("\nWelcome to AI Tic-Tac-Toe.\nThe computer only learns by " +
        "playing against itself!\n(Playing AI version {0})\n\n".format(
            ai_version if ai_version >= 0 else get_latest_ai_version()
        ), 1400)

    play_game(board_start, player_start)

    while confirm("Do you want to play again?"):
        play_game()


def play_game(board: 'list[int]'=None, human_player_id: int=None):

    if board == None:
        game = GameState(board=[0, 0, 0, 0, 0, 0, 0, 0, 0])
    else:
        game = GameState(board=board)

    if human_player_id == None:
        human_player_id = (1 if random.random() < 0.5 else -1)
        cool_type("Randomly choosing the first player: ", 8000)
    else:
        starting_player = game.whose_turn()
        if (starting_player != 0): 
            game.next_player = starting_player
        else:
            print("WARNING! Starting state is invalid.")

    spin(1)

    cool_type("You are {0}! ({1} will go first.)\n".format(*(["X", "You"] if 
        human_player_id == 1 else ["O", "AI"])), 8000)

    while (game.get_winner() == 0):
        moves = game.get_valid_moves()
        if (len(moves) == 0):
            break

        if (game.next_player == human_player_id):
            # Your turn
            move = get_valid_human_move(game, dev)
            game.move(move)
        else:
            # AI's turn
            cool_type("\nAI is thinking...  ", 5000)
            spin(0.5)
            print("     ")
            move = get_ai_move(game, state_values, 0, master)
            game.move(move)
            

    winner = game.get_winner()

    print(str(game))

    if winner == human_player_id:
        cool_type("You won! Congratulations.", 6000)
    elif winner != 0:
        cool_type("Looks like the AI won again. Better luck next time.", 6000)
    else:
        cool_type("This game ended in a draw. Nice work.", 6000)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()
        pass
    