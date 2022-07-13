from pathlib import Path
from chia.types.blockchain_format.program import Program
from clvm.casts import int_to_bytes
from clvm_tools.binutils import disassemble
from clvm_tools.clvmc import compile_clvm_text

import sys
sys.path.insert(0, "..")
import singleton_helpers_v1_1

def load_program(file_path, search_paths):
    clsp = Path(file_path).read_text()
    return Program(
        compile_clvm_text(clsp, search_paths)
    )

def print_program(program):
    print(disassemble(program))