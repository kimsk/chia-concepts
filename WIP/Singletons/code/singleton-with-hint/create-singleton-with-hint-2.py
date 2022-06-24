# ❯ cdv rpc coinrecords --by puzzlehash 5a86c9d644cedd16fd6ad64008d6bd81b28179756debaeb02e2065d97f183a60 -nd
# {
#     "dbc3ca8273d52643d68b22e35d64b08903fc4cae9452a049d8676fefb448125d": {
#         "coin": {
#             "amount": 1000000000000,
#             "parent_coin_info": "0xacdcec40696b9286c69ef86e4b425ad399fd9cb4780ff3e1a45bd4b2dcda53d1",
#             "puzzle_hash": "0x5a86c9d644cedd16fd6ad64008d6bd81b28179756debaeb02e2065d97f183a60"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 911020,
#         "spent_block_index": 921058,
#         "timestamp": 1651387251
#     },
#     ...
# }

# Launcher Coin
# ❯ cdv rpc coinrecords --by parentid dbc3ca8273d52643d68b22e35d64b08903fc4cae9452a049d8676fefb448125d -nd
# {
#     "fb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec": {
#         "coin": {
#             "amount": 1023,
#             "parent_coin_info": "0xdbc3ca8273d52643d68b22e35d64b08903fc4cae9452a049d8676fefb448125d",
#             "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 921058,
#         "spent_block_index": 921058,
#         "timestamp": 1651572021
#     },
# }


# Eve Coin
# ❯ cdv rpc coinrecords --by puzzlehash 0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d -nd
# {
#     "b3c911ef11cc78f6cc86277cbbd43e6be3a01986f88a97a00556b856e09e6b27": {
#         "coin": {
#             "amount": 1023,
#             "parent_coin_info": "0xfb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec",
#             "puzzle_hash": "0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 921058,
#         "spent_block_index": 0,
#         "timestamp": 1651572021
#     }
# }

###########
# Spend Eve
###########
from ast import Assert
import sys
from typing import List, Tuple
sys.path.insert(0, "../../../shared")

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
from cdv.util.load_clvm import load_clvm

from clvm.casts import int_to_bytes

import full_node
import wallet
import utils

# to spend a singleton, we have to know
# 1. launcher_id
launcher_id = bytes32.fromhex("fb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec")
# print(f'launcher_id: {launcher_id}')

# 2. starting coin pk to get adapted_puzzle_hash
fingerprint = 1848951423
wallet_hd_path = [12381, 8444, 2, 2]

wallet_pk: G1Element = wallet.get_public_key(fingerprint, wallet_hd_path)
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet_pk)
adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)
adapted_puzzle_hash: bytes32 = adapted_puzzle.get_tree_hash()

# print(f'wallet_pk: {wallet_pk}')
# print(f'adapted_puzzle_hash: {adapted_puzzle_hash}')
# launcher_id: eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9
# wallet_pk: 95a830e619b2922946a9b7abe915d65b871f1a6f8494dcb619c95792bb7ba774f7ce562f5437ca64db49b5ff04e205f3
# adapted_puzzle_hash: a926d2b9e40f6f08301d2f714e270bdf585a205dc7a9b83daa98afee0a1e61cd

# 3. coin id of the starting coin to calculate LineageProof
launcher_coin = full_node.get_coin_record_by_name(launcher_id).coin
assert launcher_coin != None
# print(f'launcher_coin: {launcher_coin}')

# Find the eve coin
# 1. parent id is launcher_id
coins = full_node.get_coin_records_by_parent_ids([launcher_id]) 
# 2. amount is odd
eve = next(c.coin for c in coins if c.coin.amount%2 != 0)
# print(f'eve coin:\n{eve}\n')

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
# print(f'eve lineage_proof:\n{lineage_proof}\n')

# eve lineage_proof:
# {'amount': 1023,
#  'inner_puzzle_hash': None,
#  'parent_name': '0xdbc3ca8273d52643d68b22e35d64b08903fc4cae9452a049d8676fefb448125d'}

delegated_puzzle: Program = Program.to(
    (
        1,
        [
            [
                ConditionOpcode.CREATE_COIN,
                adapted_puzzle_hash,
                1023,
                [launcher_id] # hint
            ],
        ],
    )
)
inner_solution: Program = Program.to([[], delegated_puzzle, []])

SINGLETON_MOD: Program = load_clvm(
    "singleton_top_layer_with_hint.clsp", 
    package_or_requirement=__name__, 
    search_paths=["../include"]
)
SINGLETON_MOD_HASH = SINGLETON_MOD.get_tree_hash()
puzzle_reveal: Program = SINGLETON_MOD.curry(
        (SINGLETON_MOD_HASH, (launcher_id, singleton_top_layer.SINGLETON_LAUNCHER_HASH)),
        adapted_puzzle,
    )

full_solution: Program = singleton_top_layer.solution_for_singleton(
    lineage_proof,
    eve.amount,
    inner_solution,
)
# (
#     (0xdbc3ca8273d52643d68b22e35d64b08903fc4cae9452a049d8676fefb448125d 1023) 
#     1023 
#     (
#         () 
#         (q 
#             (
#                 51 
#                 0xa926d2b9e40f6f08301d2f714e270bdf585a205dc7a9b83daa98afee0a1e61cd 
#                 1023 
#                 (0xfb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec)
#             )) ()
#     )
# )

eve_coin_spend = CoinSpend(
    eve,
    puzzle_reveal,
    full_solution,
)

sig = wallet.get_signature(
    fingerprint, 
    wallet_hd_path,
    (
        delegated_puzzle.get_tree_hash()
        + eve.name()
        + bytes32.fromhex(full_node.genesis_challenge)
    )
)

eve_spend_bundle = SpendBundle(
    [eve_coin_spend],
    sig
)

# result = full_node.push_tx(eve_spend_bundle)
# print(f'eve spend result:\n{result}\n')
# {'status': 'SUCCESS', 'success': True}

# utils.print_json(eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
# cdv inspect spendbundles $spend_bundle -db -sd -n testnet10
# (
#     (ASSERT_MY_COIN_ID 0xb3c911ef11cc78f6cc86277cbbd43e6be3a01986f88a97a00556b856e09e6b27) 
#     (AGG_SIG_ME 0xa93879400a4a293c3d6a27683185df422f59d7b633417d28fdb13bc1874a08845e5d0ac123001e440da32c5c4d74306e 0xf712f040b7e75f93fe46ccec969d50b84212ad570892eea56f03cb53d62060bd) 
#     (CREATE_COIN 0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d 1023 (0xfb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec))
# )

# ❯ cdv rpc coinrecords --by puzzlehash 0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d -nd
# {
#     "b3c911ef11cc78f6cc86277cbbd43e6be3a01986f88a97a00556b856e09e6b27": {
#         "coin": {
#             "amount": 1023,
#             "parent_coin_info": "0xfb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec",
#             "puzzle_hash": "0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 921058,
#         "spent_block_index": 937722,
#         "timestamp": 1651572021
#     },
#     "e1db0b634a30cd618604f584b09ceffe1084a3a5270f0eb7f7369f011b6c0097": {
#         "coin": {
#             "amount": 1023,
#             "parent_coin_info": "0xb3c911ef11cc78f6cc86277cbbd43e6be3a01986f88a97a00556b856e09e6b27",
#             "puzzle_hash": "0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 937722,
#         "spent_block_index": 0,
#         "timestamp": 1651863491
#     }
# }

# ❯ cdv rpc coinrecords --by hint fb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec -nd
# {
#     "e1db0b634a30cd618604f584b09ceffe1084a3a5270f0eb7f7369f011b6c0097": {
#         "coin": {
#             "amount": 1023,
#             "parent_coin_info": "0xb3c911ef11cc78f6cc86277cbbd43e6be3a01986f88a97a00556b856e09e6b27",
#             "puzzle_hash": "0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 937722,
#         "spent_block_index": 0,
#         "timestamp": 1651863491
#     }
# }

# ❯ chia rpc full_node get_coin_records_by_parent_ids '{\"include_spent_coins\": true, \"parent_ids\": [\"0xfb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec\", \"0xb3c911ef11cc78f6cc86277cbbd43e6be3a01986f88a97a00556b856e09e6b27\"]}'
# {
#     "coin_records": [
#         {
#             "coin": {
#                 "amount": 1023,
#                 "parent_coin_info": "0xfb6762bdf3e78d0b4979366c5805ce1e0f78052c643dc0ac43781b2d53edf6ec",
#                 "puzzle_hash": "0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d"
#             },
#             "coinbase": false,
#             "confirmed_block_index": 921058,
#             "spent": true,
#             "spent_block_index": 937722,
#             "timestamp": 1651572021
#         },
#         {
#             "coin": {
#                 "amount": 1023,
#                 "parent_coin_info": "0xb3c911ef11cc78f6cc86277cbbd43e6be3a01986f88a97a00556b856e09e6b27",
#                 "puzzle_hash": "0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d"
#             },
#             "coinbase": false,
#             "confirmed_block_index": 937722,
#             "spent": false,
#             "spent_block_index": 0,
#             "timestamp": 1651863491
#         }
#     ],
#     "success": true
# }
