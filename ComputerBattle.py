from AI import get_ai_move
from TicTacToe import GameState, get_game_from_int, is_valid_state
from Interface import confirm, input_number
from Files import get_pickle, save_pickle
import sys, math

PRINT_EVERY = 2000
LEARNING_RATE = 10
BOUND_RATIO = 10

# Probability of X winning (draw = 0.5)
state_values = [0.5 for _ in range(0, 3 ** 9)]

def main():
    global state_values, trial_count, x_win, o_win, last_history 
    global history_repetition

    max_trials, parent = parse_args(sys.argv)

    populate_games_end()

    if parent == None:
        pickle_open_res = get_pickle()
    else: 
        pickle_open_res = get_pickle(ask_confirm=False, use_version=parent)

    if pickle_open_res != None:
        state_values = pickle_open_res
    
    trial_count = 0

    x_win = 0
    o_win = 0

    x_win_batch = 0
    o_win_batch = 0

    if max_trials == None:
        max_trials = -1
        if confirm("do you want to limit the number of trials?"):
            max_trials = input_number("enter the maximum number of " + \
                "trials you wish to run")

    while max_trials < 0 or trial_count < max_trials:

        # Play a game of Tic-Tac-Toe
        game = GameState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        state_history = [game.to_integer()]

        while (game.get_winner() == 0):

            chosen_move = get_ai_move(game, state_values, get_step_size() * 
                BOUND_RATIO)

            if (chosen_move == None):
                break

            game.move(chosen_move)
            state_history.append(game.to_integer())

        # After the game is over

        trial_count += 1
        winner = game.get_winner()

        if (winner == 1): 
            x_win += 1
            x_win_batch += 1
        if (winner == -1):
            o_win += 1
            o_win_batch += 1

        if (winner != 0):
            for index in reversed(range(0, len(state_history))):
                if index < len(state_history) - 1:

                    current_state_id = state_history[index]
                    next_state_id = state_history[index + 1]
                    
                    state_values[current_state_id] += \
                        get_step_size() * (state_values[next_state_id] - 
                            state_values[current_state_id])

        if trial_count % PRINT_EVERY == 0:
            print(get_output() + " (This batch: X/O/D = " +
                f"{round(x_win_batch / PRINT_EVERY * 100, 2)}% " + 
                f"{round(o_win_batch / PRINT_EVERY * 100, 2)}% " + 
                f"""{round((PRINT_EVERY - x_win_batch - o_win_batch) 
                    / PRINT_EVERY * 100, 2)}%)""" +
                "         \r", end="")
            x_win_batch = 0
            o_win_batch = 0

    # After trials are complete
    print(get_output() + "\n")
    call_save_pickle()

def populate_games_end():
    global state_values

    x_wins, o_wins, games = 0, 0, 0

    for i in range (0, 3 ** 9):
        game = get_game_from_int(i)
        if is_valid_state(game):
            winner = game.get_winner()
            if winner == 1:
                # X has won
                state_values[i] = 1
                x_wins += 1
            elif winner == -1:
                # X cannot win
                state_values[i] = 0
                o_wins += 1
            games += 1

    print(f"Explored {games} games: X wins {x_wins}, O wins {o_wins}")

def get_step_size() -> float:
    return LEARNING_RATE * 1 / (50 + (0.01 * trial_count))
    
def get_output() -> str:
    return (f"{trial_count} trials completed. X wins " + 
        f"{round(x_win / trial_count * 100, 2)}%, O wins " + 
        f"{round(o_win / trial_count * 100, 2)}%, draws " + 
        f"{round((trial_count - x_win - o_win) / trial_count * 100, 2)}%")

def call_save_pickle():
    global state_values
    save_pickle(state_values, get_output() +
        f"Ran with learning rate {LEARNING_RATE}.")

def parse_args(argv: 'list[str]') -> tuple:
    trials = None
    parent = None
    try:
        if(len(argv) > 1):
            trials = int(argv[1])
            if(len(argv) > 2):
                parent = int(argv[2])
        else: 
            print("usage: <trials> <parent ai>\nSpecial values: " + 
            "-1 = infinite trials // -1 = most recent AI | -2 = no AI parent")
    except:
        pass
    return trials, parent

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        call_save_pickle()
        print()
