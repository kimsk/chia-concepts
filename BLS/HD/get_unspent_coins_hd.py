import json
import sys
sys.path.insert(0, "../../shared")

from typing import List
from blspy import (G1Element)
from chia.types.coin_record import CoinRecord
from chia.util import (bech32m)
from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle
)
import full_node
import wallet

NUM_KEYS = 50

# Get keys
fingerprint = 1848951423
hd_path = [12381, 8444, 2]
pk: G1Element = wallet.get_public_key(fingerprint, hd_path)

def get_puzzle_hash(pk: G1Element):
    return p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(pk).get_tree_hash()

def get_address(puzzhash):
    return bech32m.encode_puzzle_hash(puzzhash, "txch")

pks: List[G1Element] = wallet.get_observer_keys(pk, hd_path,  NUM_KEYS)
puzzle_hashes = list(
    map(get_puzzle_hash, pks)
)

# for ph in puzzle_hashes:
#     print(get_address(ph))

coin_records: List[CoinRecord] = full_node.get_coin_records_by_puzzle_hashes(puzzle_hashes)

cr_dict = {}
for cr in coin_records:
    address = get_address(cr.coin.puzzle_hash)
    if cr.spent_block_index == 0:
        if address not in cr_dict:
            cr_dict[address] = []
        cr_dict[address].append(cr.coin.to_json_dict())

print(json.dumps(cr_dict, indent=4))

balance = 0
for cr in coin_records:
    if cr.spent_block_index == 0:
        balance += cr.coin.amount
print(balance)