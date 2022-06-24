import json
def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))

import sys
sys.path.insert(0, "..")

from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)
from clvm_tools.binutils import disassemble

from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.blockchain_format.tree_hash import sha256_treehash
from chia.types.blockchain_format.program import INFINITE_COST, Program
from chia.types.coin_record import Coin
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.byte_types import hexstr_to_bytes
from chia.util.ints import uint64
from chia.util.hash import std_hash
from clvm import CLVMObject

from clvm.casts import int_to_bytes
from clvm_tools.clvmc import compile_clvm_text

from chia.util.condition_tools import (
    conditions_dict_for_solution,
    pkm_pairs_for_conditions_dict,
)
sk = "5a02209afa1c6b40e3f36f133d11e2044173bb72f417eb3de175dc0f411c660b"
pk = "966adadf2af72e4daee06479755570778370d47a289fd2afd5dd4cce8def2a396e7a1e0d2bc0fa7b58105bcbb2d3f83d"
message = "hello"
coin_clsp = '''
(mod conditions
    (include condition_codes.clib)
    (defconstant PK 0x{pk})

    (list
        (list AGG_SIG_UNSAFE PK "{message}")
        (list AGG_SIG_ME PK "{message}")
        ;conditions
    )
)
'''.format(pk=pk, message=message)
# print(coin_clsp)

# load_clvm from string
coin_mod: CLVMObject = compile_clvm_text(coin_clsp, search_paths=["../../include"])
puzzle_hash: bytes32 = sha256_treehash(coin_mod)
# print(coin_mod)
# print(puzzle_hash)
coin_mod: Program = Program(coin_mod)
 
parent_id: bytes32 = bytes32.fromhex("0000000000000000000000000000000000000000000000000000000000000000")
amount: uint64 = 1_000_000

coin_id = std_hash(
    parent_id +
    puzzle_hash +
    int_to_bytes(amount)
)
# print(coin_id)

private_key: PrivateKey = PrivateKey.from_bytes(bytes.fromhex(sk))
public_key: G1Element = G1Element .from_bytes(bytes.fromhex(pk))

message = bytes(message, "utf-8")

sig_unsafe = AugSchemeMPL.sign(private_key, message)
sig_me = AugSchemeMPL.sign(private_key,
    message + coin_id + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
)

agg_sig = AugSchemeMPL.aggregate([sig_unsafe + sig_me])


coin = Coin(parent_id, puzzle_hash, amount)
# print(coin)

solution = Program.to([])

# run puzzle
result = coin_mod.run(solution)
# print(result)
# opd
result = disassemble(result)
print(result)

coin_spend = CoinSpend(
    coin,
    coin_mod,
    solution 
)

err, conditions_dict, _ = conditions_dict_for_solution(
                            coin_spend.puzzle_reveal, coin_spend.solution, INFINITE_COST
                        )

# print(conditions_dict)

pkm_pairs = pkm_pairs_for_conditions_dict(
                conditions_dict,
                coin_spend.coin.name(),
                DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
            )

result = AugSchemeMPL.aggregate_verify(
    [public_key, public_key],
    [message, message + coin_id + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA],
    agg_sig
)
print(f'agg_sig:\t{result}')

for pk, msg in pkm_pairs:
    print(f'verify signature')
    print(str(pk))
    print(msg)
    result = AugSchemeMPL.verify(pk, msg, sig_me)
    print(f'sig_me:\t\t{result}')
    result = AugSchemeMPL.verify(pk, msg, sig_unsafe)
    print(f'sig_unsafe:\t{result}')

spend_bundle = SpendBundle([coin_spend], agg_sig)

print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
