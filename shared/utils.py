import json
from pathlib import Path

from rich.console import Console
from rich.syntax import Syntax

from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.condition_with_args import ConditionWithArgs
from chia.types.spend_bundle import SpendBundle
from chia.util.bech32m import bech32_decode, convertbits
from chia.util.condition_tools import (conditions_for_solution, parse_sexp_to_condition)
from chia.wallet.payment import Payment
from chia.wallet.puzzles.cat_loader import CAT_MOD
from chia.wallet.trading.offer import Offer
from chia.wallet.util.puzzle_compression import decompress_object_with_puzzles
from clvm_tools.binutils import disassemble
from clvm_tools.clvmc import compile_clvm_text
from clvm.casts import int_to_bytes

def get_offer_version(offer_hex):
    hrpgot, data = bech32_decode(offer_hex, max_length=len(offer_hex))
    decoded = convertbits(list(data), 5, 8, False)
    decoded_bytes = bytes(decoded)
    version = int.from_bytes(decoded_bytes[0:2], "big")
    return version

def get_cat_puzzlehash(asset_id: bytes32, inner_puzzlehash: bytes32):
    outer_puzzlehash = CAT_MOD.curry(
        CAT_MOD.get_tree_hash(),
        asset_id,
        inner_puzzlehash
    ).get_tree_hash_precalc(
        inner_puzzlehash
    )
    return outer_puzzlehash

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

def print_puzzle(puzzle: Program, tail=0):
    p = disassemble(puzzle)
    if tail == 0:
        print(p)
    else:
        print(f'...{p[(tail * -1):]}')

def condition_args_to_string(args):
    def to_str(arg):
        return disassemble(Program.to(arg))
    
    return ' '.join(map(to_str, args))

def print_conditions(puzzle: Program, solution: Program):
    cost, r = puzzle.run_with_cost(DEFAULT_CONSTANTS.MAX_BLOCK_COST_CLVM, solution)
    conditions = r.as_python()
    console = Console()
    for c in conditions:
        opcode = ConditionOpcode.from_bytes(c[0])
        console.print(Syntax(
                 f"({opcode.name} {condition_args_to_string(c[1:])})", 
                 "clojure", 
                 word_wrap=True
         ))

def print_payment(p: Payment):
    def parse_payment(p: Payment):
        c = p.as_condition()
        opcode = ConditionOpcode.from_bytes(c.first().as_python())
        return [opcode, *c.rest().as_python()]

    cp = parse_payment(p)
    Console().print(Syntax(
            f"({cp[0].name} {condition_args_to_string(cp[1:])})", 
            "clojure", 
            word_wrap=True
    ))

def print_offer(offer: Offer):
    # requested_payments
    for k,v in offer.requested_payments.items():
        print("Notarized Payment:")
        for p in v:
            print_payment(p)
            
    # conditions from bundle
    bundle = offer.bundle
    print("\nCoinSpend:")
    for csp in bundle.coin_spends:
        puzzle = csp.puzzle_reveal.to_program()
        solution = csp.solution.to_program()
        print("Coin:")
        print(csp.coin.name().hex())
        print(csp.coin)
        print("\nPuzzle")
        print_program(puzzle)
        print("\nSolution")
        print_program(solution)
        print("\nConditions")
        print_conditions(puzzle, solution)
    
    print("\n\nAdditions:")
    for c in bundle.additions():
        print(c)

    print("\nRemovals:")
    for c in bundle.removals():
        print(c) 

    # driver_dict
    print("Driver Dict:")
    for v in offer.driver_dict.values():
        print(v)

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
