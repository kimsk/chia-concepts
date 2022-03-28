import sys
sys.path.insert(0, "../../shared")

from blspy import (PrivateKey, AugSchemeMPL, G1Element)

from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.bech32m import decode_puzzle_hash, encode_puzzle_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import DEFAULT_HIDDEN_PUZZLE_HASH, calculate_synthetic_secret_key, puzzle_for_pk, puzzle_for_public_key_and_hidden_puzzle_hash

from full_node import get_coin, genesis_challenge
from utils import print_json

# randomly generated sk
# ❯ cdv inspect keys --random

# Secret Key: 20ec75503b49a7955c96484ee64654eaed200f68be4ee1583ee913b1d06e844e
# Public Key: 80b4b3d8327e7b08bed90fc400f82dac0e70a8fb89fc581a4e630f70795565b5e95c4acff632fddf4906a6d9c346b438
# Fingerprint: 666418440
# HD Path: m
sk: PrivateKey = PrivateKey.from_bytes(bytes.fromhex("20ec75503b49a7955c96484ee64654eaed200f68be4ee1583ee913b1d06e844e"))
pk: G1Element = sk.get_g1()

# find the associated wallet address
wallet_puzzle = puzzle_for_pk(pk)
wallet_puzzle_hash = wallet_puzzle.get_tree_hash()
wallet_txch = encode_puzzle_hash(wallet_puzzle_hash, "txch")

# wallet_puzzle_hash
print(wallet_puzzle_hash)
# txch1632n7skm56n0cdzqz8m5ehlqfnlc4qrr08ls9kcpuenyea9z670qge0v49
print(wallet_txch)

# 1 million mojo coin
# ❯ cdv rpc coinrecords --by puzhash d4553f42dba6a6fc344011f74cdfe04cff8a806379ff02db01e6664cf4a2d79e -nd
# {
#     "e0936fd36048611fdb500f7c7b16aad3a552575fce3eaed968769c94bb1e6820": {
#         "coin": {
#             "amount": 1000000,
#             "parent_coin_info": "0x3c2522b2843c704ca5a03af6aeae56169725607ef2f47954125e2b1c62e3310a",
#             "puzzle_hash": "0xd4553f42dba6a6fc344011f74cdfe04cff8a806379ff02db01e6664cf4a2d79e"
#         },
#         "coinbase": false,
#         "confirmed_block_index": 414191,
#         "spent": false,
#         "spent_block_index": 0,
#         "timestamp": 1641942120
#     }
# }
coin = get_coin("e0936fd36048611fdb500f7c7b16aad3a552575fce3eaed968769c94bb1e6820")
print(coin)

# break one coin to 2 coins and send to
# txch1y0mssn5lujacs5dl54cq0t55en72wre57sspaas24hvm7cl3emqs92kjwu
# txch18xpqwt2nl6ympftwm0clx9zk5jpj6rhu3h9fz3lt644jnljwnzgs9ffyx9
amount = int(coin.amount/2)
condition_args = [
    [ConditionOpcode.CREATE_COIN, decode_puzzle_hash("txch1y0mssn5lujacs5dl54cq0t55en72wre57sspaas24hvm7cl3emqs92kjwu"), amount],
    [ConditionOpcode.CREATE_COIN, decode_puzzle_hash("txch18xpqwt2nl6ympftwm0clx9zk5jpj6rhu3h9fz3lt644jnljwnzgs9ffyx9"), amount],
]
delegated_puzzle_solution = Program.to((1, condition_args))
synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
    sk,
    DEFAULT_HIDDEN_PUZZLE_HASH
)
solution = Program.to([[], delegated_puzzle_solution, []])
sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle_solution.get_tree_hash()
        + coin.name()
        # GENESIS_CHALLENGE for testenet10
        + genesis_challenge
    )
)

spend_bundle = SpendBundle(
    [
        CoinSpend(
            coin,
            puzzle_for_public_key_and_hidden_puzzle_hash(
                pk, DEFAULT_HIDDEN_PUZZLE_HASH
            ),
            solution
        )
    ],
    sig
)

print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
