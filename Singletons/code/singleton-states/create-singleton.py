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

coin = sim.get_coin_record_by_coin_id(launcher_id)
print(coin)

# {'coin': {'amount': 1023,
#           'parent_coin_info': '0x12d7b8c1654f82f2330059abc28e3240e863450706de7fdc518026f393f68bba',
#           'puzzle_hash': '0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9'},
#  'coinbase': False,
#  'confirmed_block_index': 12,
#  'spent_block_index': 12,
#  'timestamp': 1}
puzz_and_sol = sim.get_puzzle_and_solution(launcher_id, 12)
print(puzz_and_sol)

# 'coin': {'amount': 1023,
#           'parent_coin_info': '0x12d7b8c1654f82f2330059abc28e3240e863450706de7fdc518026f393f68bba',
#           'puzzle_hash': '0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9'},
#  'puzzle_reveal': '0xff02ffff01ff04ffff04ff04ffff04ff05ffff04ff0bff80808080ffff04ffff04ff0affff04ffff02ff0effff04ff02ffff04ffff04ff05ffff04ff0bffff04ff17ff80808080ff80808080ff808080ff808080ffff04ffff01ff33ff3cff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff0effff04ff02ffff04ff09ff80808080ffff02ff0effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080',
#  'solution': '0xffa0a1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3ff8203ffffffff8547726f757001ffff864e756d626572078080'}

# ❯ opd ffa0a1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3ff8203ffffffff8547726f757001ffff864e756d626572078080
# (0xa1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3 1023 (("Group" . 1) ("Number" . 7)))

coin_records = sim.get_coin_records_by_parent_ids([launcher_id])
print(coin_records[0].coin)

# {'amount': 1023,
#  'parent_coin_info': '0x6a4ba7e394f8d346deafcda74b26bcad649ed0cb691d7172b14970c4cf47a570',
#  'puzzle_hash': '0xa1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3'}

sim.end()

# utils.print_json(creating_eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
