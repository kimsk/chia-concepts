import sys
from typing import List, Tuple
sys.path.insert(0, "../../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.util.ints import uint64
from chia.wallet.lineage_proof import LineageProof
import chia.wallet.puzzles.singleton_top_layer as singleton_top_layer

from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)
from clvm.casts import int_to_bytes
from clvm_tools.clvmc import compile_clvm_text

import sim
import utils

sim.farm(sim.alice)

# Starting Coin
START_AMOUNT: uint64 = 1023
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(sim.alice.pk()) # standard tx puzzle
starting_coin: Coin = sim.get_coins_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
starting_coin = starting_coin[0].coin
assert starting_coin != None

# Adapt the puzzle to Singleton
adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)
adapted_puzzle_hash: bytes32 = adapted_puzzle.get_tree_hash()
comment: List[Tuple[str, str]] = [("Group", 1), ("Number", 7)] # key_value_list

launcher_coin = singleton_top_layer.generate_launcher_coin(starting_coin, START_AMOUNT)
launcher_id = launcher_coin.name()
print(f'launcher_id: {launcher_id}')

# Prepare singleton puzzle using provided singleton_top_layer
curried_singleton: Program = singleton_top_layer.SINGLETON_MOD.curry(
        (
            singleton_top_layer.SINGLETON_MOD_HASH, 
            (launcher_id, singleton_top_layer.SINGLETON_LAUNCHER_HASH)
        ), # SINGLETON_STRUCT
        adapted_puzzle, # INNER_PUZZLE
    )

launcher_solution = Program.to(
        [
            curried_singleton.get_tree_hash(),
            START_AMOUNT,
            comment,
        ]
    )

launch_conditions = [
    Program.to(
        [
            ConditionOpcode.CREATE_COIN,
            singleton_top_layer.SINGLETON_LAUNCHER_HASH,
            START_AMOUNT,
        ]
    ), 
    Program.to(
        [
            ConditionOpcode.CREATE_COIN,
            starting_puzzle.get_tree_hash(),
            starting_coin.amount - START_AMOUNT,
        ]
    ), # changes
    Program.to(
        [
            ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT,
            std_hash(launcher_coin.name() + launcher_solution.get_tree_hash()),
        ]
    )
]

launcher_coin_spend = CoinSpend(
        launcher_coin,
        singleton_top_layer.SINGLETON_LAUNCHER,
        launcher_solution,
    )


# Creating solution for standard transaction
delegated_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_conditions(launch_conditions)
full_solution: Program = p2_delegated_puzzle_or_hidden_puzzle.solution_for_conditions(launch_conditions)

print(launcher_solution)
print(full_solution)

starting_coin_spend = CoinSpend(
    starting_coin, # Alice's
    starting_puzzle, # standard transaction
    full_solution,
)

starting_coin_spend_sig = sim.get_signature(
    sim.alice,
    (
        delegated_puzzle.get_tree_hash()
        + starting_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

creating_eve_spend_bundle = SpendBundle(
    [
        starting_coin_spend, 
        launcher_coin_spend
    ],
    starting_coin_spend_sig
)

sim.pass_blocks(10)
result = sim.push_tx(creating_eve_spend_bundle)
print(f'creating eve spend result:\n{result}\n')

# when the new coin with launcher's puzzle hash (singleton_top_layer.SINGLETON_LAUNCHER) is created and spent
# eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9
# the observer can look at the solution (using get_puzzle_and_solution) provided to the launcher and see the key value list
# (0x0c0d126c89fc434fbf5ddbf6ad2afd1c5529a9df4f099608c6cd536d753948b2 1023 (("Group" . 1) ("Number" . 7)))
# the singleton child can also be tracked

# {
#   "puzzle_hash": "eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9",
#   "start_height": 1950158,
#   "include_spent_coins": true
# }
# ❯ chia rpc full_node get_coin_records_by_puzzle_hash -j $js
# {
#     "coin_records": [
#         {
# 2a6c4e70c32799eb1ebe5971754d50b5432d13602dbe913d047189413df5c46d                
#             "coin": {
#                 "amount": 1,
#                 "parent_coin_info": "0xb10e7583998b48380df492b6133c54048a96c96cdfb1793cd4eb3e5d840199f1",
#                 "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
#             },
#             "coinbase": false,
#             "confirmed_block_index": 1950245,
#             "spent": true,
#             "spent_block_index": 1950245,
#             "timestamp": 1652074082
#         }...
#     ]...
# }

# ❯ run '(sha256 0xb10e7583998b48380df492b6133c54048a96c96cdfb1793cd4eb3e5d840199f1 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1)'
# 0x2a6c4e70c32799eb1ebe5971754d50b5432d13602dbe913d047189413df5c46d

# ❯ @{name="0x2a6c4e70c32799eb1ebe5971754d50b5432d13602dbe913d047189413df5c46d"} | ConvertTo-Json | Set-Content $js
# ❯ chia rpc full_node get_coin_record_by_name -j $js
# {
#     "coin_record": {
#         "coin": {
#             "amount": 1,
#             "parent_coin_info": "0xb10e7583998b48380df492b6133c54048a96c96cdfb1793cd4eb3e5d840199f1",
#             "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 1950245,
#         "spent": true,
#         "spent_block_index": 1950245,
#         "timestamp": 1652074082
#     },
#     "success": true
# }


# ❯ @{coin_id="0x2a6c4e70c32799eb1ebe5971754d50b5432d13602dbe913d047189413df5c46d";height=1950245} | ConvertTo-Json | Set-Content $js
# ❯ chia rpc full_node get_puzzle_and_solution -j $js
# {
#     "coin_solution": {
#         "coin": {
#             "amount": 1,
#             "parent_coin_info": "0xb10e7583998b48380df492b6133c54048a96c96cdfb1793cd4eb3e5d840199f1",
#             "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
#         },
#         "puzzle_reveal": "0xff02ffff01ff04ffff04ff04ffff04ff05ffff04ff0bff80808080ffff04ffff04ff0affff04ffff02ff0effff04ff02ffff04ffff04ff05ffff04ff0bffff04ff17ff80808080ff80808080ff808080ff808080ffff04ffff01ff33ff3cff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff0effff04ff02ffff04ff09ff80808080ffff02ff0effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080",
#         "solution": "0xffa0a793802e86673478fe2f9004ccc8be442b2af8add4bbc74c159c62b30778a478ff01ffffff70c07201038020777fd4752a8bc8b25f8f91beedc9df49a355b9ff97cacf602818c4e69671ac5967e60957eb9ba20c9e183e50ab3c6702ec678b9562b14bb871f3f07f2b74d892f69817b5aa213625aa144c911455010000001768747470733a2f2f636869612e636f706f6f6c2e636f6d00000020ffff7483093a80ffff68a050d0c024f58f3b52c5083a81747e9eab6e9812e8f36e405949ee20e37bf604908080"
#     },
#     "success": true
# }


sim.end()

utils.print_json(creating_eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
