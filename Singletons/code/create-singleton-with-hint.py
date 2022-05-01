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
wallet_hd_path = [12381, 8444, 2, 2]
wallet_pk: G1Element = wallet.get_public_key(fingerprint, wallet_hd_path)
print(f'wallet_pk: {wallet_pk}')

# Starting Coin
START_AMOUNT: uint64 = 1023
starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet_pk)
coin_records: List[CoinRecord] = full_node.get_coin_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
starting_coin: Coin = coin_records[0].coin
assert starting_coin != None

# print(starting_coin)

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
print(f'adapted_puzzle_hash: {adapted_puzzle_hash}')

# Creating solution for standard transaction
delegated_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_conditions(conditions)
full_solution: Program = p2_delegated_puzzle_or_hidden_puzzle.solution_for_conditions(conditions)

starting_coinsol = CoinSpend(
    starting_coin, # Alice's
    starting_puzzle, # standard transaction
    full_solution,
)

starting_coinsol_sig = wallet.get_signature(
    fingerprint, 
    wallet_hd_path,
    (
        delegated_puzzle.get_tree_hash()
        + starting_coin.name()
        + bytes32.fromhex(full_node.genesis_challenge)
    )
)

creating_eve_spend_bundle = SpendBundle(
    [
        starting_coinsol, 
        launcher_coinsol
    ],
    starting_coinsol_sig
)

result = full_node.push_tx(creating_eve_spend_bundle)
print(f'eve spend result:\n{result}\n')

# Output from Starting Coin
# (AGG_SIG_ME 0xa93879400a4a293c3d6a27683185df422f59d7b633417d28fdb13bc1874a08845e5d0ac123001e440da32c5c4d74306e 0x6c2a25e4cd4a52a7ba1670c587b98efdbd9e812618967a61fb73feefa1117220)
# (CREATE_COIN 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9 1023)
# (ASSERT_COIN_ANNOUNCEMENT 0xc176fcc146cc1b3a9439825d0d2a8aae5864812d5d2eb746b7ffa41dbc92db59)

# Output from Launcher Coin
# (CREATE_COIN 0x56bbd112ed29b7fade94ed591f7d9d866facb9b50a00379275596671ef244912 1023)
# (CREATE_COIN_ANNOUNCEMENT 0x974eb4d94f913ea47f6ac0aa9fc522951342e32cb0fb402ff0455d0ffef9648f)

utils.print_json(creating_eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))


