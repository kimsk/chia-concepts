import sys
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)
from clvm_tools.binutils import disassemble
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
    DEFAULT_HIDDEN_PUZZLE_HASH, 
    calculate_synthetic_public_key, 
    calculate_synthetic_secret_key, 
    puzzle_for_public_key_and_hidden_puzzle_hash,
    calculate_synthetic_offset
)
from clvm_tools.clvmc import compile_clvm_text


from sim import alice, bob, charlie, get_coin_by_puzzle_hash, farm, get_coin, get_normal_coin_spend, push_tx, end
import utils

farm(alice)
farm(alice)
farm(bob)

# alice and bob wants to save XCH together for charlie
print(f'alice balance: {alice.balance()}')
print(f'bob balance: {bob.balance()}')
print(f'charlie balance: {charlie.balance()}')

xch = 1_000_000_000_000
amt = 2 * xch
message = "Love you!"
saving_clsp = '''
( mod ()
    (include condition_codes.clib)
    (defconstant ALICE_PK 0x{alice_pk})
    (defconstant BOB_PK 0x{bob_pk})
    (defconstant CHARLIE_PUZHASH 0x{charlie_puzhash})
    (defconstant MESSAGE "{message}")

    (list
        (list AGG_SIG_ME ALICE_PK (sha256 MESSAGE))
        (list AGG_SIG_ME BOB_PK (sha256 MESSAGE))
        (list CREATE_COIN CHARLIE_PUZHASH {amt})
    )
)
'''.format(
    alice_pk=alice.pk_, 
    bob_pk=bob.pk_, 
    charlie_puzhash=charlie.puzzle_hash, 
    message=message,
    amt=amt)
print(saving_clsp)
saving_hidden_puzzle: Program = Program(
    compile_clvm_text(saving_clsp, search_paths=["../include"])
)
saving_hidden_puzzle_hash = saving_hidden_puzzle.get_tree_hash()

print(saving_hidden_puzzle_hash)
alice_bob_agg_pk = alice.pk_ + bob.pk_
saving_puzzle = puzzle_for_public_key_and_hidden_puzzle_hash(
    alice_bob_agg_pk,
    saving_hidden_puzzle_hash
)
saving_puzzle_hash = saving_puzzle.get_tree_hash()

alice_coin = get_coin(alice, xch)
alice_spend, alice_sig_msg, alice_sig, alice_synthetic_pk = get_normal_coin_spend(
    alice, alice_coin,
    [
        # alice creates coin
        [ConditionOpcode.CREATE_COIN, saving_puzzle_hash, xch * 2],
        [ConditionOpcode.CREATE_COIN, alice.puzzle_hash, alice_coin.amount - xch],
    ])

bob_coin = get_coin(bob, xch)
bob_spend, bob_sig_msg, bob_sig, bob_synthetic_pk = get_normal_coin_spend(
    bob, bob_coin,
    [
        [ConditionOpcode.CREATE_COIN, bob.puzzle_hash, bob_coin.amount - xch],
    ])


agg_sig = AugSchemeMPL.aggregate([
            alice_sig, 
            bob_sig
        ])

spend_bundle = SpendBundle(
    [
        alice_spend,
        bob_spend
    ],
    agg_sig
)

assert AugSchemeMPL.aggregate_verify(
    [
        alice_synthetic_pk,
        bob_synthetic_pk
    ], 
    [
        alice_sig_msg,
        bob_sig_msg
    ], agg_sig)

# saving coin created
result = push_tx(spend_bundle)
saving_coin = get_coin_by_puzzle_hash(saving_puzzle_hash)[0].coin
print(f'saving_coin: {saving_coin}')
print(f'alice balance: {alice.balance()}')
print(f'bob balance: {bob.balance()}')
print(f'charlie balance: {charlie.balance()}')

# both now wants to send to charlie
solution = Program.to(
    [
        alice_bob_agg_pk, # original public key
        saving_hidden_puzzle, # hidden puzzle
        [], # solution
    ]
)

# test running
result = saving_puzzle.run(solution)
print(result)
saving_spend = CoinSpend(
        saving_coin,
        saving_puzzle,
        solution
    )

print(saving_spend)
msg = (
        std_hash(message.encode())
        + saving_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
)

print(msg)
alice_sig = AugSchemeMPL.sign(alice.sk_, msg)
bob_sig = AugSchemeMPL.sign(bob.sk_, msg)
agg_sig = alice_sig + bob_sig
assert AugSchemeMPL.aggregate_verify(
    [
        alice.pk_,
        bob.pk_
    ],
    [
        msg,
        msg
    ],
    agg_sig
)

spend_bundle = SpendBundle([saving_spend], agg_sig)

result = push_tx(spend_bundle)
print(result)
print(f'final charlie balance: {charlie.balance()}')

end()

utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
