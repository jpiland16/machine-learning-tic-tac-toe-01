# Note: this is not really artificial intelligence, I don't think.

from TicTacToe import GameState, Move, get_game_after_move
import random

def get_ai_move(game: GameState, state_values: 'list[int]', bound: int,
    master: bool=False) -> Move:
    
    moves = game.get_valid_moves()

    if(len(moves) == 0):
        return None

    optimal_move_benefit = 0

    moves_with_benefit = []

    for move in moves:
        move_benefit = state_values[get_game_after_move(game, move).to_integer()]
        if (game.next_player == -1): # If it is O's turn
            move_benefit = 1 - move_benefit
        

        moves_with_benefit.append((move, move_benefit))
        if move_benefit > optimal_move_benefit:
            optimal_move_benefit = move_benefit

    
    if master:
        benefit_array = [" " * 7 for _ in range(9)]
        for move, benefit in moves_with_benefit:
            benefit_array[move.pos] = "{:.5f}".format(benefit)
        print(("\n"
            "{0}|{1}|{2}\n" +
            "-------|-------|-------\n" +
            "{3}|{4}|{5} \n" +
            "-------|-------|-------\n" +
            "{6}|{7}|{8}\n\n[{9}]\n" ).format(*benefit_array, game.to_integer())
        )            

    possible_moves = []

    for move, benefit in moves_with_benefit:
        if optimal_move_benefit - benefit <= bound:
            possible_moves.append(move)
            
    if (len(possible_moves) == 0):
        print(benefit)

    chosen_move = possible_moves[0]
    if (len(possible_moves) > 1):
        chosen_move = possible_moves[random.randint(0, 
            len(possible_moves) - 1)]

    return chosen_move