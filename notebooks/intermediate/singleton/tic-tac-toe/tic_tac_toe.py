from pathlib import Path
from chia.types.blockchain_format.program import Program
from chia.wallet.puzzles import singleton_top_layer
from clvm.casts import int_to_bytes

#  x | o |   
# ---+---+---
#  x |   | o 
# ---+---+---
#  o |   | x 
def print_board(b):
    p = lambda v : ' ' if v == 0 else 'x' if v == 1 else 'o'
    print(f' {p(b[0])} | {p(b[1])} | {p(b[2])} ')
    print('---+---+---')
    print(f' {p(b[3])} | {p(b[4])} | {p(b[5])} ')
    print('---+---+---')
    print(f' {p(b[6])} | {p(b[7])} | {p(b[8])} ')

def get_curried_tic_tac_toe_puzzle(tic_tac_toe_puzzle, board, player):
    return tic_tac_toe_puzzle.curry(
        Program.to(board), 
        int_to_bytes(player)
    )

def get_tic_tac_toe_solution(position):
    return Program.to([position])
    
def play(curried_tic_tac_toe_puzzle, position):
    solution = get_tic_tac_toe_solution(position)
    run_result = curried_tic_tac_toe_puzzle.run(solution)
    return get_play_result(run_result)

# board_state
# -1 unplayable
#  0 playable
#  1 player 1 wins
#  2 player 2 wins
def get_play_result(run_result):
    board_state = run_result.at("f").as_int()
    run_result_list = run_result.at("rf").as_atom_list()
    result_board = list(
        map(lambda b: int.from_bytes(b, "little"), run_result_list)
    )
    return (board_state, result_board)


def get_curried_tic_tac_toe_puzzles(
    tic_tac_toe_coin_puzzle,
    player_one_hash,
    player_two_hash,
    tic_tac_toe_puzzle,
    board, 
    player):
    curried_tic_tac_toe_puzzle = get_curried_tic_tac_toe_puzzle(
        tic_tac_toe_puzzle, 
        board, 
        player
    )
    curried_tic_tac_toe_coin_puzzle = tic_tac_toe_coin_puzzle.curry(
        tic_tac_toe_coin_puzzle,
        player_one_hash,
        player_two_hash,
        curried_tic_tac_toe_puzzle
    )
    return curried_tic_tac_toe_puzzle, curried_tic_tac_toe_coin_puzzle

def get_curried_tic_tac_toe_puzzle_from_curried_coin_puzzle(curried_tic_tac_toe_coin_puzzle):
    return curried_tic_tac_toe_coin_puzzle.at("rrfrrfrrfrrfrfr")

def get_board_from_curried_tic_tac_toe_puzzle(curried_tic_tac_toe_puzzle):
    board_from_puzzle = curried_tic_tac_toe_puzzle.at("rrfrfr").as_atom_list()
    board_from_puzzle = list(
        map(lambda b: int.from_bytes(b, "little"), board_from_puzzle)
    )
    return board_from_puzzle

def get_player_from_curried_tic_tac_toe_puzzle(curried_tic_tac_toe_puzzle):
    player = curried_tic_tac_toe_puzzle.at("rrfrrfrfr").as_int()
    return player

def get_board_from_curried_tic_tac_toe_coin_puzzle(curried_tic_tac_toe_coin_puzzle):
    curried_tic_tac_toe_puzzle = get_curried_tic_tac_toe_puzzle_from_curried_coin_puzzle(curried_tic_tac_toe_coin_puzzle)
    board_from_puzzle = get_board_from_curried_tic_tac_toe_puzzle(curried_tic_tac_toe_puzzle)
    return board_from_puzzle

def get_position_from_singleton_solution(singleton_solution):
    position_from_solution = singleton_solution.at("rrfrf").as_int()
    return position_from_solution

def get_curried_coin_puzzle_from_singleton_puzzle(singleton_puzzle):
    adapted_inner_puzzle = singleton_puzzle.at("rrfrrfrfr")
    # rfr
    curried_tic_tac_toe_coin_puzzle = singleton_top_layer.remove_singleton_truth_wrapper(adapted_inner_puzzle)
    return curried_tic_tac_toe_coin_puzzle