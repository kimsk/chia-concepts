import sys
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)

from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from clvm.casts import int_to_bytes

from sim import alice, bob, charlie, dan, farm, get_normal_coin_spend, get_coin, push_tx, end
import utils

farm(alice)
farm(bob)
farm(charlie)

xch = 1_000_000_000_000 # 1 trillion mojos = 1 XCH
total_xch = 3 * xch

# extra conditions to force everyone to sign
extra_message = std_hash(int_to_bytes(total_xch))
extra_conditions = [
    [ConditionOpcode.AGG_SIG_UNSAFE, alice.pk_, extra_message],
    [ConditionOpcode.AGG_SIG_UNSAFE, bob.pk_, extra_message],
    [ConditionOpcode.AGG_SIG_UNSAFE, charlie.pk_, extra_message]
]

# each person has to sign the total amount
alice_extra_sig: G2Element = AugSchemeMPL.sign(alice.sk_, extra_message)
bob_extra_sig: G2Element = AugSchemeMPL.sign(bob.sk_, extra_message)
charlie_extra_sig: G2Element = AugSchemeMPL.sign(charlie.sk_, extra_message)

# normal spend
alice_coin = get_coin(alice, xch)
alice_spend, alice_sig_msg, alice_sig, alice_synthetic_pk = get_normal_coin_spend(
    alice, alice_coin,
    [
        [ConditionOpcode.CREATE_COIN, dan.puzzle_hash, xch],
        [ConditionOpcode.CREATE_COIN, alice.puzzle_hash, alice_coin.amount - xch],
    ] + extra_conditions)

bob_coin = get_coin(bob, xch)
bob_spend, bob_sig_msg, bob_sig, bob_synthetic_pk = get_normal_coin_spend(
    bob, bob_coin,
    [
        [ConditionOpcode.CREATE_COIN, dan.puzzle_hash, xch],
        [ConditionOpcode.CREATE_COIN, bob.puzzle_hash, bob_coin.amount - xch],
    ] + extra_conditions)

charlie_coin = get_coin(charlie, xch)
charlie_spend, charlie_sig_msg, charlie_sig, charlie_synthetic_pk = get_normal_coin_spend(
    charlie, charlie_coin,
    [
        [ConditionOpcode.CREATE_COIN, dan.puzzle_hash, xch],
        [ConditionOpcode.CREATE_COIN, charlie.puzzle_hash, charlie_coin.amount - xch],
    ] + extra_conditions)

# every AGG_SIG_* has to have assoicated signature aggregated
# normal spend signatures
agg_sig = AugSchemeMPL.aggregate([
        alice_sig, 
        bob_sig, 
        charlie_sig]
)
# extra signatures from each person are aggregated
agg_sig = AugSchemeMPL.aggregate([agg_sig, alice_extra_sig, alice_extra_sig, alice_extra_sig])
agg_sig = AugSchemeMPL.aggregate([agg_sig, bob_extra_sig, bob_extra_sig, bob_extra_sig])
agg_sig = AugSchemeMPL.aggregate([agg_sig, charlie_extra_sig, charlie_extra_sig, charlie_extra_sig])

# node will verify every AGG_SIG_*
aggregate_verify_result = AugSchemeMPL.aggregate_verify(
    [
        alice_synthetic_pk, 
        bob_synthetic_pk, 
        charlie_synthetic_pk, 
        alice.pk_,
        bob.pk_,
        charlie.pk_,
        alice.pk_,
        bob.pk_,
        charlie.pk_,
        alice.pk_,
        bob.pk_,
        charlie.pk_
    ], 
    [
        alice_sig_msg,
        bob_sig_msg,
        charlie_sig_msg,
        extra_message,
        extra_message,
        extra_message,
        extra_message,
        extra_message,
        extra_message,
        extra_message,
        extra_message,
        extra_message
    ], 
    agg_sig)
print(f'signature verification: {aggregate_verify_result}')

spend_bundle = SpendBundle(
    [
        alice_spend,
        bob_spend,
        charlie_spend
    ],
    agg_sig
)

# utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))

result = push_tx(spend_bundle)
print(f'dan balance:\t{dan.balance()}')
assert dan.balance() == 3 * xch
end()
