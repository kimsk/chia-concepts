import sys
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)
from cdv.util.load_clvm import load_clvm
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.coin import Coin
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import DEFAULT_HIDDEN_PUZZLE_HASH, calculate_synthetic_secret_key, puzzle_for_public_key_and_hidden_puzzle_hash
from clvm.casts import int_to_bytes
from clvm_tools.clvmc import compile_clvm_text

from sim import alice, bob, farm, get_coin, get_coin_by_coin_id, get_coin_by_puzzle_hash, pass_blocks, push_tx, end
import utils

farm(alice)

amt = 1_000_001
amt_bytes = int_to_bytes(amt)
alice_coin = get_coin(alice, amt)
assert alice_coin != None
print(f'alice coin:\t{alice_coin}')

# spend normal coin to create a launcher coin
# spend the launcher coin in the same spend bundle to create a singleton coin
# the normal coin assert the announcement from the launcher coin


launcher_puzzle = load_clvm("singleton_launcher.clsp", package_or_requirement=__name__, search_paths=["./include"]) 
launcher_puzzle_hash = launcher_puzzle.get_tree_hash()

# parent_coin_id + puzzle_hash + amt
launcher_coin = Coin(
            alice_coin.as_coin().name(),
            launcher_puzzle_hash,
            amt,
        )
#launcher_coin_id = std_hash(alice_coin.as_coin().name() + launcher_puzzle_hash + amt_bytes)
launcher_coin_id = launcher_coin.name()

print(f'launcher coin:\t{launcher_coin}')

###
# Inner Puzzle
###
# inner_clsp = '''
# (mod (puzzle_hash value)
#     (list
#         (list CREATE_COIN puzzle_hash value)
#     )
# )
# '''
inner_clsp = '''
()
'''

inner_puzzle: Program = Program(
    compile_clvm_text(inner_clsp, search_paths=["./include"])
)


###
# Singleton
# https://chialisp.com/docs/puzzles/singletons#the-singleton-top-layer
# https://developers.chia.net/t/new-singleton-1-1-standard-top-layer/387
# (SINGLETON_STRUCT INNER_PUZZLE lineage_proof my_amount inner_solution)
# SINGLETON_STRUCT = (MOD_HASH . (LAUNCHER_ID . LAUNCHER_PUZZLE_HASH))
# 
###
singleton_top_layer = load_clvm("singleton_top_layer_v1_1.clsp", package_or_requirement=__name__, search_paths=["./include"]) 
singleton_mod_hash = singleton_top_layer.get_tree_hash()
singleton_struct = Program.to((singleton_mod_hash, (launcher_coin_id, launcher_puzzle_hash)))
my_singleton = singleton_top_layer.curry(
    singleton_struct,
    inner_puzzle
)
my_singleton_puzzle_hash = my_singleton.get_tree_hash()


# (singleton_full_puzzle_hash amount key_value_list)
launcher_solution = Program.to([my_singleton_puzzle_hash, amt_bytes, []])
launcher_announcement = launcher_solution.get_tree_hash()


###
# spend the normal coin
###
condition_args = [
    # create a launcher coin
    [ConditionOpcode.CREATE_COIN, launcher_puzzle_hash, amt],
    # create change back to alice
    [ConditionOpcode.CREATE_COIN, alice.puzzle_hash, alice_coin.amount - amt],
    # assert announcement
    [ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT,  std_hash(launcher_coin_id + launcher_announcement)]
]

delegated_puzzle_solution = Program.to((1, condition_args))
synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
    alice.sk_,
    DEFAULT_HIDDEN_PUZZLE_HASH
)
solution = Program.to([[], delegated_puzzle_solution, []])

normal_coin_spend_sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle_solution.get_tree_hash()
        + alice_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

normal_coin_spend = CoinSpend(
            alice_coin.as_coin(),
            alice.puzzle,
            solution,
        )

###
# Launcher
###
launcher_coin_spend = CoinSpend(
    launcher_coin,
    launcher_puzzle,
    launcher_solution
)

sig = normal_coin_spend_sig
spend_bundle = SpendBundle(
    [
        normal_coin_spend,
        launcher_coin_spend
    ],
    sig,
)


push_tx(spend_bundle)

launcher_coin = get_coin_by_coin_id(launcher_coin_id)
print(f'launcher coin spent: {launcher_coin}')

my_singleton_coin_id = std_hash(launcher_coin_id + my_singleton_puzzle_hash + amt_bytes)
my_singleton_coin = get_coin_by_coin_id(my_singleton_coin_id)
print(f'singleton coin: {my_singleton_coin}')
pass_blocks(10)
## spending singleton coin
# (
#   SINGLETON_STRUCT
#   INNER_PUZZLE
#   lineage_proof
#   my_amount
#   inner_solution
# )
# lineage_proof
#   (parent_parent_coin_info parent_inner_puzzle_hash parent_amount)
#   (parent_parent_coin_info parent_amount)

singleton_solution = Program.to(
    [],
    amt,
    []
)
spend_bundle = SpendBundle(
    [
        CoinSpend(
            my_singleton_coin.coin,
            my_singleton,
            singleton_solution
        )
    ],
    G2Element(),
)

result = push_tx(spend_bundle)
print(result)
my_singleton_coin = get_coin_by_coin_id(my_singleton_coin_id)
print(f'singleton coin spent: {my_singleton_coin}')


end()
utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
