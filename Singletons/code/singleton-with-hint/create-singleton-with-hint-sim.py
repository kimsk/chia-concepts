import sys
from typing import List, Tuple
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element)
from cdv.util.load_clvm import load_clvm
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
from chia.wallet.lineage_proof import LineageProof

from chia.wallet.derive_keys import (
    _derive_path_unhardened
)
from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)
from clvm.casts import int_to_bytes

import sim
import utils

sim.farm(sim.alice)

# Starting Coin (Alice's)
START_AMOUNT: uint64 = 1023
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(sim.alice.pk())
starting_coin: Coin = sim.get_coins_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
starting_coin = starting_coin[0].coin
assert starting_coin != None


launcher_coin = singleton_top_layer.generate_launcher_coin(starting_coin, START_AMOUNT)
launcher_id = launcher_coin.name()

adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)
adapted_puzzle_hash: bytes32 = adapted_puzzle.get_tree_hash()
comment: List[Tuple[str, str]] = [("Hello", "Chia")] # key_value_list

SINGLETON_MOD: Program = load_clvm("singleton_top_layer.clsp", package_or_requirement=__name__, search_paths=["./include"])
SINGLETON_MOD_HASH = SINGLETON_MOD.get_tree_hash()

singleton_puzzle: Program = SINGLETON_MOD.curry(
        (SINGLETON_MOD_HASH, (launcher_id, singleton_top_layer.SINGLETON_LAUNCHER_HASH)),
        adapted_puzzle,
    )

curried_singleton: Program = SINGLETON_MOD.curry(
        (SINGLETON_MOD_HASH, (launcher_coin.name(), singleton_top_layer.SINGLETON_LAUNCHER_HASH)),
        adapted_puzzle,
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

# print(starting_coin)
# print(launcher_coin)
# print(SINGLETON_MOD_HASH)
# print(singleton_puzzle.get_tree_hash())
# print(launcher_coin_spend)

# Creating solution for standard transaction
delegated_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_conditions(launch_conditions)
full_solution: Program = p2_delegated_puzzle_or_hidden_puzzle.solution_for_conditions(launch_conditions)

starting_coin_spend = CoinSpend(
    starting_coin, # Alice's
    starting_puzzle, # standard transaction
    full_solution,
)

sig = sim.get_signature(sim.alice, 
    (
        delegated_puzzle.get_tree_hash()
        + starting_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

spend_bundle = SpendBundle(
    [
        starting_coin_spend,
        launcher_coin_spend
    ],
    sig

)

sim.pass_blocks(10)
result = sim.push_tx(spend_bundle)
# print(result)

# Find the singleton coin
# 1. parent id is singleton_eve
coins = sim.get_coin_records_by_parent_ids([launcher_id]) 
# 2. amount is odd
eve = next(c.coin for c in coins if c.coin.amount%2 != 0)
# print(f'eve coin:\n{eve}\n')

delegated_puzzle: Program = Program.to(
    (
        1,
        [
            [
                ConditionOpcode.CREATE_COIN,
                adapted_puzzle_hash,
                eve.amount
            ]
        ],
    )
)
inner_solution: Program = Program.to([[], delegated_puzzle, []])

#      If this is the Eve singleton:
#
#          PH = None
#          L = LineageProof(Launcher, PH, amount)
lineage_proof: LineageProof = singleton_top_layer.lineage_proof_for_coinsol(launcher_coin_spend)
# print(f'eve lineage_proof:\n{lineage_proof}\n')
assert lineage_proof == LineageProof(
    launcher_coin_spend.coin.parent_coin_info,
    None,
    START_AMOUNT
) 

puzzle_reveal: Program = SINGLETON_MOD.curry(
        (SINGLETON_MOD_HASH, (launcher_coin.name(), singleton_top_layer.SINGLETON_LAUNCHER_HASH)),
        adapted_puzzle,
    )
full_solution: Program = singleton_top_layer.solution_for_singleton(
    lineage_proof,
    eve.amount,
    inner_solution,
)

eve_coinsol = CoinSpend(
    eve,
    puzzle_reveal,
    full_solution,
)

singleton_eve_coinsol_sig = sim.get_signature(sim.alice, 
    (
        delegated_puzzle.get_tree_hash()
        + eve.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

eve_spend_bundle = SpendBundle(
    [eve_coinsol],
    singleton_eve_coinsol_sig
)

sim.pass_blocks(10)
result = sim.push_tx(eve_spend_bundle)
print(f'eve spend result:\n{result}\n')


sim.end()
# utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
# utils.print_json(eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
