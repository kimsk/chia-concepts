import sys
from typing import List, Tuple
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
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
    DEFAULT_HIDDEN_PUZZLE_HASH, 
    calculate_synthetic_secret_key, 
    puzzle_for_public_key_and_hidden_puzzle_hash,
    solution_for_hidden_puzzle
)
from clvm.casts import int_to_bytes
from clvm_tools.clvmc import compile_clvm_text

import sim 
import utils


sim.farm(sim.alice)
#   ,------------.
#   | Coin A     |
#   `------------'
#         |
#  ------------------ Atomic Transaction 1 -----------------
#         v
#   .------------.       .-------------------------------.
#   | Launcher   |------>| Eve Coin Containing Program I |
#   `------------'       `-------------------------------'


# Consider that you have some coin A that you want to create a singleton
# containing some inner puzzle I from with amount T.  We'll call the Launcher
# coin, which is created from A "Launcher" and the first iteration of the
# singleton, called the "Eve" spend, Eve.  When spent, I yields a coin
# running I' and so on in a singleton specific way described below.
T = 1023
alice_coin = sim.get_coin(sim.alice, T)
assert alice_coin != None

inner_clsp = '''
(mod (singleton_amt my_amt to_puzhash)
    (include condition_codes.clib)

    (list
        (list CREATE_COIN to_puzhash singleton_amt)
        (list CREATE_COIN to_puzhash (- my_amt singleton_amt))
        (list ASSERT_MY_AMOUNT my_amt)
    )
)
'''

I = singleton_puzzles.adapt_inner_to_singleton(Program(
    compile_clvm_text(inner_clsp, search_paths=["./include"])
))

# 1) Designate some coin as coin A
A = alice_coin.as_coin()

# 2) call puzzle_for_singleton with that coin's name (it is the Parent of the
#    Launch coin), and the initial inner puzzle I, curried as appropriate for
#    its own purpose. Adaptations of the program I and its descendants are
#    required as below.
Launcher = singleton_puzzles.generate_launcher_coin(A, T)
singleton_puzzle = singleton_puzzles.puzzle_for_singleton(Launcher.name(), I)

# 3) call launch_conditions_and_coinsol to get a set of "launch_conditions",
#    which will be used to spend standard coin A, and a "spend", which spends
#    the Launcher created by the application of "launch_conditions" to A in a
#    spend. These actions must be done in the same spend bundle.
comment: List[Tuple[str, str]] = [("Hello", "Chia")]
launch_conditions, launcher_coin_spend = singleton_puzzles.launch_conditions_and_coinsol(
    alice_coin,
    I,
    comment,
    T
)

#    One can create a SpendBundle containing the spend of A giving it the
#    argument list (() (q . launch_conditions) ()) and then append "spend" onto
#    its .coin_spends to create a combined spend bundle.
delegated_puzzle_solution = Program.to((1, launch_conditions))
A_coin_spend = CoinSpend(
    A,
    puzzle_for_public_key_and_hidden_puzzle_hash(
        sim.alice.pk(), DEFAULT_HIDDEN_PUZZLE_HASH
    ),
    Program.to([[], delegated_puzzle_solution, []])
)
synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
    sim.alice.sk_,
    DEFAULT_HIDDEN_PUZZLE_HASH
)
A_coin_spend_sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle_solution.get_tree_hash()
        + A.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

spend_bundle = SpendBundle(
    [
        A_coin_spend,
        launcher_coin_spend
    ],
    A_coin_spend_sig,
)

print(f'T: {T}\n')
print(f'I: {I.get_tree_hash()}\n{I}\n')
print(f'A:\n{A.name()}\n{A}\n')
print(f'Launcher:\n{Launcher.name()}\n{Launcher}\n')
# print(f'Create Singleton Spend Bundle:\n{spend_bundle}')

# A's conditions:
#   (AGG_SIG_ME 0xa042c855d234578415254b7870b711fb25e8f85beaa4a66bd0673d394c761fa156406c2e3bb375d5b18766d2a12cc918 0x31603f83103be735370fa93e02b8e4ed9fdc12d859c756597f964d287a4985a5)
#   (CREATE_COIN 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 0x0f42bb)
#   (ASSERT_COIN_ANNOUNCEMENT 0x168887c50fb7175284d0ea9b894e3e78a7cff58afdade103d7c79bbcf2f98c46)
# Launcher's conditions:
#   (CREATE_COIN 0xc2571cd93ef0c4f1bfc8d0b7c4d5eeb091f38bf1ad7831083108d1bcf4d54df0 0x0f42bb)
#   (CREATE_COIN_ANNOUNCEMENT 0xba15964450f499b53ace054a6ddd8cb7dfbef0d8f9724baafea4f3645d00b997)

sim.pass_blocks(10)
result = sim.push_tx(spend_bundle)
print(f'creating singleton spend result:\n{result}\n')

# The first iteration of the singleton, called the "Eve" spend is created
# eve_id = Coin(Launcher.name(), puzzle_for_singleton(Launcher.name(), I), amount)
launcher_id = Launcher.name()
eve_id = std_hash(
    launcher_id + 
    singleton_puzzle.get_tree_hash() + 
    int_to_bytes(T)
)

eve = sim.get_coin_record_by_coin_id(eve_id)
assert eve.coin.name() == eve_id
assert eve.coin.amount == T
print(f'Eve:\n{eve.coin.name()}\n{eve}\n')

# The singleton adds an ASSERT_MY_COIN_ID to constrain it to the coin that
# matches its own conception of itself.  It consumes a "LineageProof" object
# when spent that must be constructed so.  We'll call the singleton we intend
# to spend "S".
S = eve.coin
#      If this is the Eve singleton:
#
#          PH = None
#          L = LineageProof(Launcher, PH, amount)
#
#       - Note: the Eve singleton's .parent_coin_info should match Launcher here.
PH = None
L = LineageProof(Launcher.parent_coin_info, PH, T)
assert L == singleton_puzzles.lineage_proof_for_coinsol(launcher_coin_spend)

AI = Program.to([113, T, sim.alice.puzzle_hash])
S_solution = singleton_puzzles.solution_for_singleton(L, T, AI)

eve_coin_spend = CoinSpend(
            S,
            singleton_puzzle,
            S_solution
        )

eve_spend_bundle = SpendBundle(
    [
        eve_coin_spend
    ],
    G2Element()
)

sim.pass_blocks(10)
result = sim.push_tx(eve_spend_bundle)
print(f'creating eve spend result:\n{result}\n')

#   (ASSERT_MY_COIN_ID 0x4736b9ea6888bcee89cb9b6c3c8aabfe3a9aa700787f2c70b825599c4db19fce)
#   (CREATE_COIN 0x3395fea33edf7597d62f84b3fc642580dc514d65d52f728512225813e01c91b2 113) ; new singleton
#   (CREATE_COIN 0x4f45877796d7a64e192bcc9f899afeedae391f71af3afd7e15a0792c049d23d3 910) ; send to Alice
#   (ASSERT_MY_AMOUNT 1023) ; extra condition
print(f'alice balance:\n{sim.alice.balance()}\n')

# looking for a new singleton coin
# 1. parent is the eve coin
coins = sim.get_coin_records_by_parent_ids([eve_id])
# 2. amount is odd
S1 = next(c.coin for c in coins if c.coin.amount%2 != 0)
print(f'S1:\n{S1}\n')


#  --------------- (2) Transaction With I ------------------/
#                                        |                     
#                                        v                     
#                 .-----------------------------------.
#                 | Running Singleton With Program I' |
#                 `-----------------------------------'
#                                        |
# --------------------- End Transaction 2 ------------------
# == To spend the singleton requires some host side setup ==
#
# spend second singleton
#          PH = ParentOf(S).inner_puzzle_hash
#          L = LineageProof(ParentOf(S).name(), PH, amount)
#
#       - Note: ParentOf(S).name is the .parent_coin_info member of the
#         coin record for S.
# PH = I.get_tree_hash()
# # ParentOf(S).name()
# T = 113
# L1 = LineageProof(S.parent_coin_info, PH, T)
L1 = singleton_puzzles.lineage_proof_for_coinsol(eve_coin_spend)
# assert L1 == L1_
print(f'L1:\n{L1}\n')

AI = Program.to([13, 110, sim.alice.puzzle_hash])
S_puzzle = singleton_puzzles.puzzle_for_singleton(S1.name(), I.get_tree_hash())


delegated_puzzle: Program = Program.to(
                (
                    1,
                    [
                        [
                            ConditionOpcode.CREATE_COIN,
                            I.get_tree_hash(),
                            S.amount,
                        ]
                    ],
                )
            )
inner_solution: Program = Program.to([[], delegated_puzzle, []])
S1_solution = singleton_puzzles.solution_for_singleton(
    L1, 
    S1.amount, 
    inner_solution
)

s1_coin_spend = CoinSpend(
            S1,
            S_puzzle,
            S_solution
        )

s1_spend_bundle = SpendBundle(
    [
        s1_coin_spend
    ],
    G2Element()
)
sim.pass_blocks(10)
result = sim.push_tx(s1_spend_bundle)
print(f'creating s1 spend result:\n{result}\n')

sim.end()
# utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
# utils.print_json(eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
