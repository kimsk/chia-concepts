import sys
from typing import List
sys.path.insert(0, "../../shared")

from blspy import (G1Element)
from chia.types.coin_record import CoinRecord
from chia.util import (bech32m)
from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle
)
import full_node
import wallet

# Get keys
fingerprint = 1848951423
hd_path = [12381, 8444, 2]
pk: G1Element = wallet.get_public_key(fingerprint, hd_path)

def get_puzzle_hash(pk: G1Element):
    return p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(pk).get_tree_hash()

def get_address(puzzhash):
    return bech32m.encode_puzzle_hash(puzzhash, "txch")

pks: List[G1Element] = wallet.get_observer_keys(pk, hd_path,  5000)
puzzle_hashes = list(
    map(get_puzzle_hash, pks)
)

# for ph in puzzle_hashes:
#     print(get_address(ph))

coin_records: List[CoinRecord] = full_node.get_coin_records_by_puzzle_hashes(puzzle_hashes)

balance = 0
for cr in coin_records:
    if cr.spent_block_index != 0:
        balance += cr.coin.amount
print(balance)