from blspy import (PrivateKey, AugSchemeMPL, G1Element)
from chia.types.blockchain_format.program import Program
from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle
)

# Wallet public key 0 (m/12381/8444/2/0): 98a7f4315186bceb8a03ed2079394ab3c32d4b0a5ab6bf4d0b3754bfb8b30787d33ed25a24b411c52de84d3a69ccceb0
# Wallet private key 0 (m/12381/8444/2/0): 3b18495d94d81d52bb8e63a6115c507d0bd50979269ee4a6f0e7b5d158f4c065
pk = "98a7f4315186bceb8a03ed2079394ab3c32d4b0a5ab6bf4d0b3754bfb8b30787d33ed25a24b411c52de84d3a69ccceb0"
pk_: G1Element = G1Element.from_bytes(bytes.fromhex(pk))
print(pk_)

puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(pk_)
print(puzzle.get_tree_hash())

synthetic_pk: G1Element = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_public_key(pk_, p2_delegated_puzzle_or_hidden_puzzle.DEFAULT_HIDDEN_PUZZLE_HASH)

print(synthetic_pk)
# 0xa89431b6661954eeee68758a38b7ce6325cdc7f76c88eb0aa954c67f36936ef6436bbe3596174e883bf3533267be6f9b

# DID
pk = ""

# synthetic_pk
# 0x9683a4c279f5ad66bc2548ad4de9130b15eb17565bf3f3f3474f58b243c133760a09593d66386cdfbd69eefd58befc51