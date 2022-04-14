import sys
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.coin import Coin
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.wallet.lineage_proof import LineageProof
import chia.wallet.puzzles.singleton_top_layer as singleton_puzzles
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import DEFAULT_HIDDEN_PUZZLE_HASH, calculate_synthetic_secret_key, puzzle_for_public_key_and_hidden_puzzle_hash
from clvm.casts import int_to_bytes
from clvm_tools.clvmc import compile_clvm_text

import sim 
import utils


sim.farm(sim.alice)

amt = 1_000_000
start_amt = 1_023
# 1) Designate some coin as coin A
alice_coin = sim.get_coin(sim.alice, amt)
assert alice_coin != None
print(f'alice coin:\t{alice_coin}')

inner_clsp = '''
( mod ()
    (include condition_codes.clib)
    (defconstant BOB_PUZHASH 0x{bob_puzhash})

    (list
        (list CREATE_COIN BOB_PUZHASH {amt})
    )
)
'''.format(
    bob_puzhash=sim.bob.puzzle_hash, 
    amt=start_amt)

print(inner_clsp)

inner_puzzle: Program = Program(
    compile_clvm_text(inner_clsp, search_paths=["./include"])
)

# 2) call puzzle_for_singleton with that coin's name (it is the Parent of the
#    Launch coin), and the initial inner puzzle I, curried as appropriate for
#    its own purpose. Adaptations of the program I and its descendants are
#    required as below.

# 3) call launch_conditions_and_coinsol to get a set of "launch_conditions",
#    which will be used to spend standard coin A, and a "spend", which spends
#    the Launcher created by the application of "launch_conditions" to A in a
#    spend. These actions must be done in the same spend bundle.
launch_conditions, launcher_coin_spend = singleton_puzzles.launch_conditions_and_coinsol(
    alice_coin,
    inner_puzzle,
    Program.to([]),
    start_amt)


print(f'launch_conditions:\t{launch_conditions}')
# (51 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1023)
# (61 0x413445ff6a343415e9e77127ba3feab87f648fe677da466625b2a8c0d0ccfff5)
print(f'launcher_coin_spend:\t{launcher_coin_spend}')
# solution:
# (singleton_full_puzzle_hash amount key_value_list)
# (0x4b5bf198c591a5902abf71bb4c998233030c3a5be45360ccabacbb4a584aad67 1023 ())

#    One can create a SpendBundle containing the spend of A giving it the
#    argument list (() (q . launch_conditions) ()) and then append "spend" onto
#    its .coin_spends to create a combined spend bundle.
delegated_puzzle_solution = Program.to((1, launch_conditions))
alice_coin_spend = CoinSpend(
            alice_coin.as_coin(),
            sim.alice.puzzle,
            Program.to([[], delegated_puzzle_solution, []])
        )
synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
    sim.alice.sk_,
    DEFAULT_HIDDEN_PUZZLE_HASH
)
alice_coin_spend_sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle_solution.get_tree_hash()
        + alice_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

spend_bundle = SpendBundle(
    [
        alice_coin_spend,
        launcher_coin_spend
    ],
    alice_coin_spend_sig,
)

sim.pass_blocks(10)
sim.push_tx(spend_bundle)

# alice_coin spent output conditions
#   (AGG_SIG_ME 0xa042c855d234578415254b7870b711fb25e8f85beaa4a66bd0673d394c761fa156406c2e3bb375d5b18766d2a12cc918 0xe737a88067a8a759b3ee5c01c188cf70b7530ed0aa0bee95bc6e56ec00603d73)
#   (CREATE_COIN 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1023)
#   (ASSERT_COIN_ANNOUNCEMENT 0x413445ff6a343415e9e77127ba3feab87f648fe677da466625b2a8c0d0ccfff5)

# laucnher_coin spend output conditions
#   (CREATE_COIN 0x4b5bf198c591a5902abf71bb4c998233030c3a5be45360ccabacbb4a584aad67 1023)
#   (CREATE_COIN_ANNOUNCEMENT 0xbbd91e928a77897bf76b637b948576a1d3976e214423cf11da38009f9ac1dccd)

# launcher_puzzle_hash: 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9
# singleton_puzzle_hash: 0x4b5bf198c591a5902abf71bb4c998233030c3a5be45360ccabacbb4a584aad67


launcher_id = launcher_coin_spend.coin.name()
launcher_coin = sim.get_coin_by_coin_id(launcher_id)
print(f'launcher coin spent: {launcher_coin}')

singleton_puzzle = singleton_puzzles.puzzle_for_singleton(launcher_id, inner_puzzle)
singleton_coin_id = std_hash(launcher_id + singleton_puzzle.get_tree_hash() + int_to_bytes(launcher_coin_spend.coin.amount))
singleton_coin = sim.get_coin_by_coin_id(singleton_coin_id)
print(f'singleton coin: {singleton_coin}')


# Spend the Eve (or first?) singleton
lineage_proof: LineageProof = singleton_puzzles.lineage_proof_for_coinsol(launcher_coin_spend) 
print(lineage_proof)
singleton_solution = singleton_puzzles.solution_for_singleton(lineage_proof, start_amt, [])
print(singleton_solution)

singleton_spend_bundle = SpendBundle(
    [
        CoinSpend(
            singleton_coin.coin,
            singleton_puzzle,
            singleton_solution
        )
    ],
    G2Element() # empty signature
)
sim.pass_blocks(10)
sim.push_tx(singleton_spend_bundle)
singleton_coin = sim.get_coin_by_coin_id(singleton_coin_id)
print(f'singleton coin spent: {singleton_coin}')
sim.pass_blocks(10)

sim.farm(farmer=sim.charlie)

a_coin = sim.get_coin_by_puzzle_hash(bytes.fromhex("597814e2aa3ff4a04ac1af152cb67077f15e5d2a3dc9de7f39b2ddda5721e2e2"))
print(a_coin)
sim.end()
# utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
utils.print_json(singleton_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
