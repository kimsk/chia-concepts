from pathlib import Path
from chia.types.blockchain_format.program import Program
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
    
def play(curried_tic_tac_toe_puzzle, position):
    solution = Program.to([position])
    run_result = curried_tic_tac_toe_puzzle.run(solution)
    return get_play_result(run_result)

def get_play_result(run_result):
    is_winning = bool(run_result.at("f").as_int())
    run_result_list = run_result.at("rf").as_atom_list()
    result_board = list(
        map(lambda b: int.from_bytes(b, "little"), run_result_list)
    )
    return (is_winning, result_board)

