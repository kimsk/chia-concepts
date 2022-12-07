import json
from pathlib import Path

from rich.console import Console
from rich.syntax import Syntax

from chia.types.blockchain_format.program import Program
from clvm.casts import int_to_bytes
from clvm_tools.binutils import disassemble
from clvm_tools.clvmc import compile_clvm_text


def load_program(file_path, search_paths):
    clsp = Path(file_path).read_text()
    return Program(
        compile_clvm_text(clsp, search_paths)
    )

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
