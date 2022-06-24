import sys
from typing import List, Tuple
sys.path.insert(0, "../../../shared")

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
from chia.wallet.derive_keys import (
    _derive_path_unhardened
)
from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)
from clvm.casts import int_to_bytes

import full_node
import wallet
import utils

# Get keys
fingerprint = 1848951423
wallet_hd_path = [12381, 8444, 2, 2]
wallet_pk: G1Element = wallet.get_public_key(fingerprint, wallet_hd_path)
print(f'wallet_pk: {wallet_pk}')

# Starting Coin
START_AMOUNT: uint64 = 1023
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet_pk)
coin_records: List[CoinRecord] = full_node.get_coin_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
starting_coin: Coin = next(cr.coin for cr in coin_records if cr.spent == False)
assert starting_coin != None

print(starting_coin)
# Adapt the puzzle to Singleton
adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)
adapted_puzzle_hash: bytes32 = adapted_puzzle.get_tree_hash()
comment: List[Tuple[str, str]] = [("Hello", "Chia")] # key_value_list

SINGLETON_MOD: Program = load_clvm(
    "singleton_top_layer_with_hint.clsp", 
    package_or_requirement=__name__, 
    search_paths=["../include"]
)
SINGLETON_MOD_HASH = SINGLETON_MOD.get_tree_hash()

launcher_coin = singleton_top_layer.generate_launcher_coin(starting_coin, START_AMOUNT)
launcher_id = launcher_coin.name()

print(f'Launcher Id: {launcher_id}\n')
print(f'adapted_puzzle_hash: {adapted_puzzle_hash}')

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

print(starting_coin)
print(launcher_coin)
print(SINGLETON_MOD_HASH)
print(singleton_puzzle.get_tree_hash())
print(launcher_coin_spend)

# Creating solution for standard transaction
delegated_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_conditions(launch_conditions)
full_solution: Program = p2_delegated_puzzle_or_hidden_puzzle.solution_for_conditions(launch_conditions)

starting_coin_spend = CoinSpend(
    starting_coin, # Alice's
    starting_puzzle, # standard transaction
    full_solution,
)

starting_coin_spend_sig = wallet.get_signature(
    fingerprint, 
    wallet_hd_path,
    (
        delegated_puzzle.get_tree_hash()
        + starting_coin.name()
        + bytes32.fromhex(full_node.genesis_challenge)
    )
)

creating_eve_spend_bundle = SpendBundle(
    [
        starting_coin_spend, 
        launcher_coin_spend
    ],
    starting_coin_spend_sig
)

# result = full_node.push_tx(creating_eve_spend_bundle)
# print(f'eve spend result:\n{result}\n')

# Output from Starting Coin
#   (AGG_SIG_ME 0xa93879400a4a293c3d6a27683185df422f59d7b633417d28fdb13bc1874a08845e5d0ac123001e440da32c5c4d74306e 0x3e0a6dc63e756491ebdbeb61c4aa47433a58f0328e87ab2817159343fa782295)
#   (CREATE_COIN 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1023)
#   (CREATE_COIN 0x5a86c9d644cedd16fd6ad64008d6bd81b28179756debaeb02e2065d97f183a60 0x00e8d4a50c01)
#   (ASSERT_COIN_ANNOUNCEMENT 0xe0eb7a06941a1c1300c81d4e694a8fc9d2ae94e19a39df7589760b63801965c3)

# Output from Launcher Coin
#   (CREATE_COIN 0x1f8bc8c41b16efed4d067fd0927a018a228b4ef83e6767553e8a8798b00b0c4d 1023)
#   (CREATE_COIN_ANNOUNCEMENT 0x88ce7c866c2b4c4357093473d77e45294c8cdbe1e71e406a6b45b721989df750)
# utils.print_json(creating_eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))


