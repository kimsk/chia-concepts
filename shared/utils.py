import json
from pathlib import Path

from rich.console import Console
from rich.syntax import Syntax

from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.spend_bundle import SpendBundle
from chia.util.bech32m import bech32_decode, convertbits
from chia.util.condition_tools import conditions_for_solution
from chia.wallet.util.puzzle_compression import decompress_object_with_puzzles
from clvm_tools.binutils import disassemble
from clvm_tools.clvmc import compile_clvm_text
from clvm.casts import int_to_bytes


def load_program(file_path, search_paths):
    clsp = Path(file_path).read_text()
    return Program(
        compile_clvm_text(clsp, search_paths)
    )

def load_hex(file_path):
    hex_str = Path(file_path).read_text()
    return Program.fromhex(hex_str)

def print_clsp(clsp: str, line_numbers=True):
    console = Console()
    syntax = Syntax(clsp, "clojure", line_numbers=line_numbers, word_wrap=True)
    console.print(syntax)

def print_program(program: Program):
    p = disassemble(program)
    console = Console()
    syntax = Syntax(p, "clojure", line_numbers=False, word_wrap=True)
    console.print(syntax)

def print_puzzle(puzzle, tail=0):
    p = disassemble(puzzle)
    if tail == 0:
        print(p)
    else:
        print(f'...{p[(tail * -1):]}')

def print_conditions(puzzle, solution):
    error, conditions, cost = conditions_for_solution(
            puzzle, 
            solution, 
            DEFAULT_CONSTANTS.MAX_BLOCK_COST_CLVM
    )
    def to_str(c_vars):
        return disassemble(Program.to(c_vars))

    console = Console()
    if error is None:
        for c in conditions:
            if len(c.vars) == 1:
                console.print(Syntax(
                    f"({c.opcode.name} {to_str(c.vars[0])})", 
                    "clojure", 
                    word_wrap=True
                ))
            if len(c.vars) == 2:
                console.print(Syntax(
                    f"({c.opcode.name} {to_str(c.vars[0])} {to_str(c.vars[1])})",
                    "clojure",
                    word_wrap=True,
                ))
    else:
        console.print(f"[bold red]{error}")

def print_push_tx_result(result):
    print("additions:")
    print("==========")
    for addition in result["additions"]:
        print(addition)
        
    print("removals:")
    print("=========")
    for removal in result["removals"]:
        print(removal)

def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))

def print_offer(offer_hex: str):
    hrpgot, data = bech32_decode(offer_hex, max_length=len(offer_hex))
    if hrpgot != 'offer':
        raise ValueError('hex string is not an offer')
    
    decoded = convertbits(list(data), 5, 8, False)
    decoded_bytes = bytes(decoded)
    decompressed_bytes = decompress_object_with_puzzles(decoded_bytes)
    bundle = SpendBundle.from_bytes(decompressed_bytes)

    for csp in bundle.coin_solutions:
        coin = csp.coin
        puzzle = csp.puzzle_reveal.to_program()
        solution = csp.solution.to_program()
        print(coin)
        if coin.amount == 0:
            continue
        print(coin.name().hex())
        print_conditions(puzzle, solution)