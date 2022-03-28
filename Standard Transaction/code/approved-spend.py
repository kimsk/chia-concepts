from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import DEFAULT_HIDDEN_PUZZLE_HASH, calculate_synthetic_secret_key, puzzle_for_public_key_and_hidden_puzzle_hash
from clvm_tools import binutils

from sim import alice, bob, charlie, farm, get_coin, push_tx, end
from utils import print_json

farm(alice)

amt = 1_000_000_000
fee = 1_000_000

alice_coin = get_coin(alice, amt, fee)
assert alice_coin != None
print(f'alice coin:\t{alice_coin}')

# alice want to send coin to charlie, but bob has to approve the amount and the recipient of the spend as well
# alice acquires bob's pk and create conditions to create coins for charlie and herself
condition_args = [
    [ConditionOpcode.AGG_SIG_ME, bob.pk(), std_hash(bytes(amt) + charlie.puzzle_hash)],
    [ConditionOpcode.CREATE_COIN, charlie.puzzle_hash, amt],
    # send change back to alice
    [ConditionOpcode.CREATE_COIN, alice.puzzle_hash, (alice_coin.amount) - (amt + fee)]
]

# 1 is the clvm of `(mod conditions conditions)`
delegated_puzzle_solution = Program.to((1, condition_args))
solution = Program.to([[], delegated_puzzle_solution, []])

synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
    alice.sk_,
    DEFAULT_HIDDEN_PUZZLE_HASH
)
synthetic_pk: G1Element = synthetic_sk.get_g1()
print(f"synthetic_pk:\t{synthetic_pk}")

# alice verifies the conditions
result = alice.puzzle.run(solution)
print(f'conditions :\n{binutils.disassemble(result)}')
# (c (list AGG_SIG_ME SYNTHETIC_PUBLIC_KEY (sha256tree delegated_puzzle)) conditions)
# (   
#     (50 0xb50b02adba343fff8bf3a94e92ed7df43743aedf0006b81a6c00ae573c0cce7d08216f60886fe84e4078a5209b0e5171 0xda09fcfdd86c8c15112b5aa4d9f51c12bf19bf0ea58bbc7d805eadb41088ea80)
#     (50 0x8f0347a04e231f6e93716eddf281632562af3e947096731532a813da10ce9b4f4a29b36f8a9f102a62d61e5dedbd9ce2 0xce377c6635cf3ba8077e4f7aa93694af06426e2b4e2a501ad2a7686319a5c3ed)
#     (51 0x0df91132d84844398d71426cb4026ca006af9630de48d4acb22df1c04b43be4d 0x3b9aca00)
#     (51 0x4eb7420f8651b09124e1d40cdc49eeddacbaa0c25e6ae5a0a482fac8e3b5259f 0x01973876cfc0)
# )

# alice sign the hash of delegated_puzzle_solution with synthetic private key
alice_sig: G2Element = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle_solution.get_tree_hash()
        + alice_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

unapproved_spend_bundle = SpendBundle(
    [
        CoinSpend(
            alice_coin.as_coin(),
            alice.puzzle,
            solution,
        )
    ],
    alice_sig,
)

# spend bundle with alice's signature only won't work
result = push_tx(unapproved_spend_bundle)
assert result['error'] == 'Err.BAD_AGGREGATE_SIGNATURE'

# later the spend bundle and synthetic pk is sent to bob
# bob verifies the delegated_puzzle_solution hash
assert AugSchemeMPL.verify(synthetic_pk,
    delegated_puzzle_solution.get_tree_hash()
    + alice_coin.name()
    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
    alice_sig
)

# bob approve the amount to be sent to charlie
bob_sig = AugSchemeMPL.sign(bob.sk_,
    (   std_hash(bytes(amt) + charlie.puzzle_hash)
        + alice_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

# aggregate two alice's and bob's signature
agg_sig = AugSchemeMPL.aggregate([alice_sig, bob_sig])
print(f"alice sig:\t{alice_sig}")
print(f"bob sig:\t{bob_sig}")
print(f"agg sig:\t{agg_sig}")

# # bob replace alice_sig with the agg_sig
approved_spend_bundle = SpendBundle(
    [
        CoinSpend(
            alice_coin.as_coin(),
            alice.puzzle,
            solution,
        )
    ],
    agg_sig,
)

result = push_tx(approved_spend_bundle)
print(f'alice balance:\t\t{alice.balance()}')
print(f'charlie balance:\t{charlie.balance()}')
print_json(approved_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
end()
