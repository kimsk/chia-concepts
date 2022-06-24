from blspy import (AugSchemeMPL, G1Element, G2Element, PrivateKey)
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
    calculate_synthetic_offset,
    calculate_synthetic_secret_key, 
    calculate_synthetic_public_key, 
    DEFAULT_HIDDEN_PUZZLE_HASH)

from keys import *
from messages import *

print(f'pk1:\t\t\t{pk1}')

# synthetic
print(f'hidden puzzle hash:\t{DEFAULT_HIDDEN_PUZZLE_HASH}')

# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.py#L41
# synthetic_offset = sha256(hidden_puzzle_hash + original_public_key)
synthetic_offset: int = calculate_synthetic_offset(pk1, DEFAULT_HIDDEN_PUZZLE_HASH)

# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.py#L48
# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/calculate_synthetic_public_key.clvm
# synthentic_public_key = original_public_key + synthetic_offset_pubkey
# (point_add public_key (pubkey_for_exp (sha256 public_key hidden_puzzle_hash)))
# https://chialisp.com/docs/ref/clvm#bls12-381-operators
synthetic_pk: G1Element = calculate_synthetic_public_key(pk1, DEFAULT_HIDDEN_PUZZLE_HASH)

# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.py#L53
synthetic_sk: PrivateKey = calculate_synthetic_secret_key(sk1, DEFAULT_HIDDEN_PUZZLE_HASH)
print(f'synthetic_offset:\t{synthetic_offset}')
print(f'synthetic_pk:\t\t{synthetic_pk}')

print(f'sk1:\t\t\t{sk1}')
print(f'synthetic_sk:\t\t{synthetic_sk}')


sig: G2Element = AugSchemeMPL.sign(synthetic_sk, m1)
assert AugSchemeMPL.verify(synthetic_pk, m1, sig)