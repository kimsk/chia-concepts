import sys
from typing import List, Tuple
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element)
from chia.types.blockchain_format.coin import Coin
from chia.types.coin_record import CoinRecord
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
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

# Get keys
fingerprint = 1848951423
master_sk: PrivateKey = PrivateKey.from_bytes(bytes.fromhex(wallet.get_private_key(fingerprint)['sk']))
wallet_hd_path = [12381, 8444, 2, 2]
wallet_sk: PrivateKey = _derive_path_unhardened(master_sk, wallet_hd_path)
wallet_pk: G1Element = wallet_sk.get_g1()

# Starting Coin
START_AMOUNT: uint64 = 1023
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet_pk)
coin_records: List[CoinRecord] = full_node.get_coin_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
starting_coin: Coin = coin_records[0].coin
assert starting_coin != None

print(starting_coin)

# Adapt the puzzle to Singleton
adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)
adapted_puzzle_hash: bytes32 = adapted_puzzle.get_tree_hash()
comment: List[Tuple[str, str]] = [("Hello", "Chia")] # key_value_list
conditions, launcher_coinsol = singleton_top_layer.launch_conditions_and_coinsol(
                    starting_coin, 
                    adapted_puzzle, 
                    comment, 
                    START_AMOUNT
                )

launcher_id = std_hash(
    starting_coin.name() +
    singleton_top_layer.SINGLETON_LAUNCHER_HASH + 
    int_to_bytes(START_AMOUNT)
) 
assert launcher_id == launcher_coinsol.coin.name()
print(f'Launcher Id: {launcher_id}\n')