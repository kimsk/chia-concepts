from pathlib import Path
from chia.types.blockchain_format.program import Program
from clvm.casts import int_to_bytes
from clvm_tools.clvmc import compile_clvm_text

import sys
sys.path.insert(0, "..")
import singleton_helpers_v1_1

def load_program(file_path, search_paths):
    clsp = Path(file_path).read_text()
    return Program(
        compile_clvm_text(clsp, search_paths)
    )

def load_puzzle():
    tic_tac_toe_puzzle = load_program('tic-tac-toe.clsp', '.')
    return tic_tac_toe_puzzle

def load_coin_puzzle():
    tic_tac_toe_coin_puzzle = load_program('tic-tac-toe-coin.clsp', '.')
    return tic_tac_toe_coin_puzzle

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

def get_curried_puzzle(puzzle, board, player):
    return puzzle.curry(
        Program.to(board), 
        int_to_bytes(player)
    )

def get_solution(position):
    return Program.to([position])
    
def play(curried_puzzle, position):
    solution = get_solution(position)
    run_result = curried_puzzle.run(solution)
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


def get_curried_puzzles(
    coin_puzzle,
    player_one_hash,
    player_two_hash,
    puzzle,
    board, 
    player):
    curried_puzzle = get_curried_puzzle(
        puzzle, 
        board, 
        player
    )
    curried_coin_puzzle = coin_puzzle.curry(
        coin_puzzle,
        player_one_hash,
        player_two_hash,
        curried_puzzle
    )
    return curried_puzzle, curried_coin_puzzle

def get_curried_puzzle_from_curried_coin_puzzle(curried_coin_puzzle):
    return curried_coin_puzzle.at("rrfrrfrrfrrfrfr")

def get_board_from_curried_puzzle(curried_puzzle):
    board_from_puzzle = curried_puzzle.at("rrfrfr").as_atom_list()
    board_from_puzzle = list(
        map(lambda b: int.from_bytes(b, "little"), board_from_puzzle)
    )
    return board_from_puzzle

def get_player_from_curried_puzzle(curried_puzzle):
    player = curried_puzzle.at("rrfrrfrfr").as_int()
    return player

def get_board_from_curried_coin_puzzle(curried_coin_puzzle):
    curried_puzzle = get_curried_puzzle_from_curried_coin_puzzle(curried_coin_puzzle)
    board_from_puzzle = get_board_from_curried_puzzle(curried_puzzle)
    return board_from_puzzle

def get_player_from_curried_coin_puzzle(curried_coin_puzzle):
    curried_puzzle = get_curried_puzzle_from_curried_coin_puzzle(curried_coin_puzzle)
    player_from_puzzle = get_player_from_curried_puzzle(curried_puzzle)
    return player_from_puzzle

def get_position_from_singleton_solution(singleton_solution):
    position_from_solution = singleton_solution.at("rrfrf").as_int()
    return position_from_solution

def get_curried_coin_puzzle_from_singleton_puzzle(singleton_puzzle):
    curried_coin_puzzle = singleton_puzzle.at("rrfrrfrfr")
    return curried_coin_puzzle

async def get_current_state(get_coin_records_by_parent_ids, get_coin_record_by_name, get_puzzle_and_solution, launcher_id):
    singleton_coin = await singleton_helpers_v1_1.get_unspent_singleton(get_coin_records_by_parent_ids, launcher_id)
    parent_id = singleton_coin.parent_coin_info
    parent_coin_record = await get_coin_record_by_name(parent_id)
    spent_block_index = parent_coin_record.spent_block_index
    coin_spent = await get_puzzle_and_solution(parent_id, spent_block_index)

    singleton_puzzle = coin_spent.puzzle_reveal.to_program()
    singleton_solution = coin_spent.solution.to_program()

    curried_coin_puzzle = get_curried_coin_puzzle_from_singleton_puzzle(singleton_puzzle)
    curried_puzzle = get_curried_puzzle_from_curried_coin_puzzle(curried_coin_puzzle)
    position_from_solution = get_position_from_singleton_solution(singleton_solution)
    result, current_board = play(curried_puzzle, position_from_solution)
    return result, current_board
