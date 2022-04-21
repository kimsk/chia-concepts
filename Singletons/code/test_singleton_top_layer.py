# https://github.com/Chia-Network/release-test-chia-blockchain/blob/02a880fbac6f0c304b84b6f485d10af2251f7dbc/tests/clvm/test_singletons.py

import sys
from typing import List, Tuple
sys.path.insert(0, "../../shared")

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
    p2_conditions,
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)
from clvm.casts import int_to_bytes
from clvm_tools.clvmc import compile_clvm_text

import sim 
import utils

sim.farm(sim.alice)
print(sim.get_height())

START_AMOUNT: uint64 = 1023
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(sim.alice.pk())
starting_coin: Coin = sim.get_coins_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
starting_coin = starting_coin[0].coin
assert starting_coin != None

adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)
adapted_puzzle_hash: bytes32 = adapted_puzzle.get_tree_hash()

comment: List[Tuple[str, str]] = [("Hello", "Chia")]
conditions, launcher_coinsol = singleton_top_layer.launch_conditions_and_coinsol(
                    starting_coin, 
                    adapted_puzzle, 
                    comment, 
                    START_AMOUNT
                )
# conditions
# (51 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1023)
# (61 0x8ab82db728f2a32e7e08d3eac960577c43f9fab99c3baacb2e4f1d54db2dfa3c)

# Creating solution for standard transaction
delegated_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_conditions(conditions)
full_solution: Program = p2_delegated_puzzle_or_hidden_puzzle.solution_for_conditions(conditions)

starting_coinsol = CoinSpend(
    starting_coin, # Alice's
    starting_puzzle, # standard transaction
    full_solution,
)

synthetic_sk: PrivateKey = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_secret_key(
    sim.alice.sk_,
    p2_delegated_puzzle_or_hidden_puzzle.DEFAULT_HIDDEN_PUZZLE_HASH
)

starting_coinsol_sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle.get_tree_hash()
        + starting_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

spend_bundle = SpendBundle(
    [
        starting_coinsol, 
        launcher_coinsol
    ],
    starting_coinsol_sig
)
sim.pass_blocks(10)
result = sim.push_tx(spend_bundle)
print(f'creating singleton spend result:\n{result}\n')

# consuming coin (0xe3b0c44298fc1c149afbf4c8996fb92400000000000000000000000000000001 0x4f45877796d7a64e192bcc9f899afeedae391f71af3afd7e15a0792c049d23d3 0x01977420dc00)
#   with id 12d7b8c1654f82f2330059abc28e3240e863450706de7fdc518026f393f68bba
#   (AGG_SIG_ME 0xa042c855d234578415254b7870b711fb25e8f85beaa4a66bd0673d394c761fa156406c2e3bb375d5b18766d2a12cc918 0xd274fe1a50233f7c000f1d05a44f5ced983c263f9f7fe46b12467f560d1c47c8)
#   (CREATE_COIN 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1023)
#   (ASSERT_COIN_ANNOUNCEMENT 0x20d559f6551da1382b4d2ba96cc604685b43f2782aa2153f01fafda77f37de7f)

# consuming coin (0x12d7b8c1654f82f2330059abc28e3240e863450706de7fdc518026f393f68bba 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1023)
#  with id 6a4ba7e394f8d346deafcda74b26bcad649ed0cb691d7172b14970c4cf47a570 
#   (CREATE_COIN 0xa1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3 1023)
#   (CREATE_COIN_ANNOUNCEMENT 0x427e7b5c7a03d854ba1596ba76dad1b21738c9a2d120ee45152e3c4647f60859)

# Spend Eve
launcher_id = launcher_coinsol.coin.name()
singleton_puzzle = singleton_top_layer.puzzle_for_singleton(launcher_id, adapted_puzzle)

singleton_eve_id = std_hash(
    launcher_id + 
    singleton_puzzle.get_tree_hash() + 
    int_to_bytes(START_AMOUNT)
)
singleton_eve = sim.get_coin_record_by_coin_id(singleton_eve_id).coin
# print(launcher_id)
# print(eve_id)
# print(eve)
# print(sim.get_all_non_reward_coins())

delegated_puzzle: Program = Program.to(
    (
        1,
        [
            [
                ConditionOpcode.CREATE_COIN,
                adapted_puzzle_hash,
                singleton_eve.amount,
            ]
        ],
    )
)
inner_solution: Program = Program.to([[], delegated_puzzle, []])
# Generate the lineage proof we will need from the launcher coin
lineage_proof: LineageProof = singleton_top_layer.lineage_proof_for_coinsol(launcher_coinsol)
puzzle_reveal: Program = singleton_top_layer.puzzle_for_singleton(
    launcher_id,
    adapted_puzzle,
)
full_solution: Program = singleton_top_layer.solution_for_singleton(
    lineage_proof,
    singleton_eve.amount,
    inner_solution,
)

singleton_eve_coinsol = CoinSpend(
    singleton_eve,
    puzzle_reveal,
    full_solution,
)

synthetic_sk: PrivateKey = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_secret_key(
    sim.alice.sk_,
    p2_delegated_puzzle_or_hidden_puzzle.DEFAULT_HIDDEN_PUZZLE_HASH
)

singleton_eve_coinsol_sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle.get_tree_hash()
        + singleton_eve.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

eve_spend_bundle = SpendBundle(
    [singleton_eve_coinsol],
    singleton_eve_coinsol_sig
)

sim.pass_blocks(10)
result = sim.push_tx(eve_spend_bundle)
print(f'singleton eve spend result:\n{result}\n')


# POST-EVE
# 1. parent id is singleton_eve
coins = sim.get_coin_records_by_parent_ids([singleton_eve.name()]) 
# 2. amount is odd
singleton = next(c.coin for c in coins if c.coin.amount%2 != 0)
# print(f'singleton:\n{singleton}\n')

lineage_proof: LineageProof = singleton_top_layer.lineage_proof_for_coinsol(singleton_eve_coinsol)

# Same puzzle_reveal too
full_solution: Program = singleton_top_layer.solution_for_singleton(
    lineage_proof,
    singleton.amount,
    inner_solution,
)

singleton_coinsol = CoinSpend(
    singleton,
    puzzle_reveal,
    full_solution,
)

synthetic_sk: PrivateKey = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_secret_key(
    sim.alice.sk_,
    p2_delegated_puzzle_or_hidden_puzzle.DEFAULT_HIDDEN_PUZZLE_HASH
)

singleton_coinsol_sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle.get_tree_hash()
        + singleton.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

singleton_spend_bundle = SpendBundle(
    [singleton_coinsol],
    singleton_coinsol_sig
)

sim.pass_blocks(10)
result = sim.push_tx(singleton_spend_bundle)
print(f'singleton spend result:\n{result}\n')


sim.end()
# utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
# utils.print_json(eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
