# Starting Coin
# ❯ cdv rpc coinrecords --by id 0101a581331ee609668229b75a08fb6f3bb32abf15349acc11c17c2072643a8d      
# [
#     {
#         "coin": {
#             "amount": 1000000000000,
#             "parent_coin_info": "0xb5a447de3372535aa7fe3a237c899e081197206f06507d9a68a04463f38c5f04",
#             "puzzle_hash": "0x5a86c9d644cedd16fd6ad64008d6bd81b28179756debaeb02e2065d97f183a60"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 892119,
#         "spent_block_index": 905698,
#         "timestamp": 1651030300
#     }
# ]

# Launcher Coin
# ❯ cdv rpc coinrecords --by parentid 0101a581331ee609668229b75a08fb6f3bb32abf15349acc11c17c2072643a8d
# [
#     {
#         "coin": {
#             "amount": 1023,
#             "parent_coin_info": "0x0101a581331ee609668229b75a08fb6f3bb32abf15349acc11c17c2072643a8d",
#             "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 905698,
#         "spent_block_index": 905698,
#         "timestamp": 1651284177
#     }
# ]


# Eve Coin
# ❯ cdv rpc coinrecords --by puzzlehash 0x56bbd112ed29b7fade94ed591f7d9d866facb9b50a00379275596671ef244912 
# [
#     {
#         "coin": {
#             "amount": 1023,
#             "parent_coin_info": "0x2defa04144fef9c90598cba104f36e2922c1b0c99220223780d6da561b874a7a",
#             "puzzle_hash": "0x56bbd112ed29b7fade94ed591f7d9d866facb9b50a00379275596671ef244912"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 905698,
#         "spent_block_index": 0,
#         "timestamp": 1651284177
#     }
# ]

###########
# Spend Eve
###########
from ast import Assert
import sys
from typing import List, Tuple
sys.path.insert(0, "../../shared")

from blspy import (AugSchemeMPL, G1Element)
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.coin import Coin
from chia.types.coin_record import CoinRecord
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.util.ints import uint64
from chia.wallet.derive_keys import (
    _derive_path_unhardened
)
from chia.wallet.lineage_proof import LineageProof

from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)
from clvm.casts import int_to_bytes

import full_node
import wallet
import utils

# to spend a singleton, we have to know
# 1. launcher_id
launcher_id = bytes32.fromhex("2defa04144fef9c90598cba104f36e2922c1b0c99220223780d6da561b874a7a")
print(f'launcher_id: {launcher_id}')

# 2. starting coin pk to get adapted_puzzle_hash
fingerprint = 1848951423
wallet_hd_path = [12381, 8444, 2, 2]

wallet_pk: G1Element = wallet.get_public_key(fingerprint, wallet_hd_path)
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet_pk)
adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)
adapted_puzzle_hash: bytes32 = adapted_puzzle.get_tree_hash()

print(f'wallet_pk: {wallet_pk}')
print(f'adapted_puzzle_hash: {adapted_puzzle_hash}')
# launcher_id: 2defa04144fef9c90598cba104f36e2922c1b0c99220223780d6da561b874a7a
# wallet_pk: 95a830e619b2922946a9b7abe915d65b871f1a6f8494dcb619c95792bb7ba774f7ce562f5437ca64db49b5ff04e205f3
# adapted_puzzle_hash: a926d2b9e40f6f08301d2f714e270bdf585a205dc7a9b83daa98afee0a1e61cd

# 3. coin id of the starting coin to calculate LineageProof
launcher_coin = full_node.get_coin_record_by_name(launcher_id).coin
assert launcher_coin != None
print(f'launcher_coin: {launcher_coin}')

# Find the eve coin
# 1. parent id is launcher_id
coins = full_node.get_coin_records_by_parent_ids([launcher_id]) 
# 2. amount is odd
eve = next(c.coin for c in coins if c.coin.amount%2 != 0)
print(f'eve coin:\n{eve}\n')
# eve coin:
# {'amount': 1023,
#  'parent_coin_info': '0x2defa04144fef9c90598cba104f36e2922c1b0c99220223780d6da561b874a7a',
#  'puzzle_hash': '0x56bbd112ed29b7fade94ed591f7d9d866facb9b50a00379275596671ef244912'}

#      If this is the Eve singleton:
#
#          PH = None
#          L = LineageProof(Launcher, PH, amount)
lineage_proof: LineageProof = LineageProof(
    launcher_coin.parent_coin_info,
    None,
    eve.amount
)
print(f'eve lineage_proof:\n{lineage_proof}\n')
# eve lineage_proof:
# {'amount': 1023,
#  'inner_puzzle_hash': None,
#  'parent_name': '0x0101a581331ee609668229b75a08fb6f3bb32abf15349acc11c17c2072643a8d'}

delegated_puzzle: Program = Program.to(
    (
        1,
        [
            [
                ConditionOpcode.CREATE_COIN,
                adapted_puzzle_hash,
                1001,
                [launcher_id] # hint
            ],
            # txch1hynzxczjkwffz992zm565r564pzl9f5y60wfna867lxd7j9ystsqgmfsgm
            # b926236052b3929114aa16e9aa0e9aa845f2a684d3dc99f4faf7ccdf48a482e0
            [
                ConditionOpcode.CREATE_COIN,
                bytes32.fromhex("b926236052b3929114aa16e9aa0e9aa845f2a684d3dc99f4faf7ccdf48a482e0"),
                22,
                [launcher_id] # hint
            ],
        ],
    )
)
inner_solution: Program = Program.to([[], delegated_puzzle, []])

puzzle_reveal: Program = singleton_top_layer.puzzle_for_singleton(
    launcher_id,
    adapted_puzzle,
)
full_solution: Program = singleton_top_layer.solution_for_singleton(
    lineage_proof,
    eve.amount,
    inner_solution,
)
# (
#     (0x0101a581331ee609668229b75a08fb6f3bb32abf15349acc11c17c2072643a8d 1023) 
#     1023 
#     (
#         () 
#         (q 
#             (
#                 51 
#                 0xa926d2b9e40f6f08301d2f714e270bdf585a205dc7a9b83daa98afee0a1e61cd 
#                 1021 
#                 0x2defa04144fef9c90598cba104f36e2922c1b0c99220223780d6da561b874a7a
#             )
#         ) ()))

eve_coinsol = CoinSpend(
    eve,
    puzzle_reveal,
    full_solution,
)

singleton_eve_coinsol_sig = wallet.get_signature(
    fingerprint, 
    wallet_hd_path,
    (
        delegated_puzzle.get_tree_hash()
        + eve.name()
        + bytes32.fromhex(full_node.genesis_challenge)
    )
)

eve_spend_bundle = SpendBundle(
    [eve_coinsol],
    singleton_eve_coinsol_sig
)

# result = full_node.push_tx(eve_spend_bundle)
# print(f'eve spend result:\n{result}\n')

utils.print_json(eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
