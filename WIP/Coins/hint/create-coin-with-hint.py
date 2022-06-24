import sys
from typing import List, Tuple
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element)
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.coin import Coin
from chia.types.coin_record import CoinRecord
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.util.ints import uint64
from chia.wallet.derive_keys import (
    _derive_path_unhardened
)
from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)
from clvm.casts import int_to_bytes

import full_node
import wallet
import utils

# Get keys
fingerprint = 1848951423
wallet_hd_path = [12381, 8444, 2, 41]
wallet_pk: G1Element = wallet.get_public_key(fingerprint, wallet_hd_path)
# print(f'wallet_pk: {wallet_pk}')

# Starting Coin
START_AMOUNT: uint64 = 1_000_000 
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet_pk)
coin_records: List[CoinRecord] = full_node.get_coin_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
starting_coin: Coin = next(cr.coin for cr in coin_records if cr.spent == False)
assert starting_coin != None

# print(f'starting_coin: {starting_coin}')

wallet_pk_41: G1Element = wallet.get_public_key(fingerprint, [12381, 8444, 2, 41])
puzzle_hash_41 = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet_pk_41).get_tree_hash()
print(puzzle_hash_41)

hint = bytes.fromhex("b23dee66835e536f7f1ce287b0837c0cb12aabfe250719cb19302db8ecceac73")

condition_args = [
    [
        ConditionOpcode.CREATE_COIN,
        puzzle_hash_41,
        starting_coin.amount - 500_000_000,
        [hint] # hint
    ]
]
delegated_puzzle = Program.to((1, condition_args))

# solution = Program.to([[], delegated_puzzle, []])
solution = p2_delegated_puzzle_or_hidden_puzzle.solution_for_delegated_puzzle(delegated_puzzle, [])
sig = wallet.get_signature(
    fingerprint,
    wallet_hd_path,
    (
        delegated_puzzle.get_tree_hash()
        + starting_coin.name()
        + bytes32.fromhex(full_node.genesis_challenge)
    )
)

coin_spend = CoinSpend(
    starting_coin,
    starting_puzzle,
    solution,
)

spend_bundle = SpendBundle(
    [coin_spend],
    sig
)

# result = full_node.push_tx(spend_bundle)
# print(f'spend result:\n{result}\n')

utils.print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))

# spend result:
# {'status': 'SUCCESS', 'success': True}

# cdv inspect spendbundles ./create-coin-with-hint-spend-bundle.json -db -sd -n testnet10