import sys
from typing import List, Tuple
sys.path.insert(0, "../../shared")

from blspy import (AugSchemeMPL, G1Element, G2Element, PrivateKey)
from chia.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
from chia.wallet.derive_keys import (
    master_sk_to_farmer_sk,
    master_sk_to_pool_sk,
    master_sk_to_wallet_sk,
    find_authentication_sk,
    find_owner_sk,
    _derive_path_unhardened
)

from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
    DEFAULT_HIDDEN_PUZZLE_HASH, 
    calculate_synthetic_secret_key,
    puzzle_for_pk, 
    puzzle_for_public_key_and_hidden_puzzle_hash
)


import full_node
import wallet
import utils

fingerprint = 1848951423
master_sk: PrivateKey = PrivateKey.from_bytes(bytes.fromhex(wallet.get_private_key(fingerprint)['sk']))

all_coins = []

for i in range(100):
    wallet_hd_path = [12381, 8444, 2, i]
    sk = _derive_path_unhardened(master_sk, wallet_hd_path)
    pk = sk.get_g1()
    wallet_puzzle_hash = puzzle_for_pk(pk).get_tree_hash()
    wallet_txch = encode_puzzle_hash(wallet_puzzle_hash, "txch")
    # print(wallet_puzzle_hash)
    coin_records = full_node.get_coin_records_by_puzzle_hash(wallet_puzzle_hash)
    all_coins += list(map(lambda cr: cr.coin, coin_records))

utils.print_json(list(map(lambda c: c.to_json_dict(), all_coins)))