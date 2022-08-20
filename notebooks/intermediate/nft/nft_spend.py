import aiosqlite
import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import sys
sys.path.insert(0, ".")
import keys_utils
import full_node


from blspy import AugSchemeMPL, G1Element, G2Element
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.condition_tools import conditions_dict_for_solution, pkm_pairs_for_conditions_dict
from chia.util.db_wrapper import DBWrapper2, execute_fetchone
from chia.util.ints import uint32
from chia.wallet.derivation_record import DerivationRecord
from chia.wallet.lineage_proof import LineageProof
from chia.wallet.nft_wallet.nft_info import IN_TRANSACTION_STATUS, NFTCoinInfo, NFTWalletInfo
from chia.wallet.nft_wallet.uncurry_nft import UncurriedNFT
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
    DEFAULT_HIDDEN_PUZZLE_HASH,
    calculate_synthetic_secret_key,
    puzzle_for_pk,
    puzzle_for_conditions,
    solution_for_conditions,
)
from chia.wallet.puzzles.puzzle_utils import (
    make_assert_absolute_seconds_exceeds_condition,
    make_assert_coin_announcement,
    make_assert_my_coin_id_condition,
    make_assert_puzzle_announcement,
    make_create_coin_announcement,
    make_create_coin_condition,
    make_create_puzzle_announcement,
    make_reserve_fee_condition,
)
from chia.wallet.util.wallet_types import AmountWithPuzzlehash, WalletType

def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))

DB_VERSION = 2
FINGERPRINT = 4096957589
DB_PATH = Path(f'/mnt/e/testnet/wallet/db/blockchain_wallet_v2_r1_testnet10_{FINGERPRINT}.sqlite')

async def get_nft_coin_info(nft_id):
    query = f"""
        SELECT nft_id, coin, lineage_proof, mint_height, status, full_puzzle, latest_height
        FROM users_nfts WHERE removed_height IS NULL and nft_id='{nft_id}'
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(query) as cursor:
            async for row in cursor:
                nft_coin_info = NFTCoinInfo(
                    bytes32.from_hexstr(row[0]),
                    Coin.from_json_dict(json.loads(row[1])),
                    None if row[2] is None else LineageProof.from_json_dict(json.loads(row[2])),
                    Program.from_bytes(row[5]),
                    uint32(row[3]),
                    uint32(row[6]) if row[6] is not None else uint32(0),
                    row[4] == IN_TRANSACTION_STATUS,
                )
                return nft_coin_info
    return None

async def get_derivation_record_for_puzzle_hash(puzzle_hash: bytes32):
    query = f"""
        SELECT derivation_index, pubkey, puzzle_hash, wallet_type, wallet_id, hardened 
        FROM derivation_paths
        WHERE puzzle_hash='{puzzle_hash.hex()}'
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(query) as cursor:
            async for row in cursor:
                derivation_record = DerivationRecord(
                    uint32(row[0]),
                    bytes32.fromhex(row[2]),
                    G1Element.from_bytes(bytes.fromhex(row[1])),
                    WalletType(row[3]),
                    uint32(row[4]),
                    bool(row[5]),
                )
                return derivation_record
    return None

async def keys_for_puzzle_hash(puzzle_hash: bytes32):
    derivation_record = await get_derivation_record_for_puzzle_hash(puzzle_hash)
    
    if derivation_record is not None:
        # wallet hd-path (m/12381/8444/2/{idx})
        hd_path = [12381, 8444, 2, derivation_record.index]
        sk = await keys_utils.get_secret_key_async(FINGERPRINT, hd_path)
        pk = sk.get_g1()
        return sk, pk 

    return None, None

async def get_xch_coin_spend_and_signature(coin_id: bytes32, to_puzzle_hash: bytes32, fee = 2_000):
    coin_record = await full_node.get_coin_record_by_name_async(coin_id)
    coin = coin_record.coin
    sk, pk = await keys_for_puzzle_hash(coin.puzzle_hash)

    puzzle_reveal = puzzle_for_pk(pk)
    conditions = [
        [ConditionOpcode.CREATE_COIN, to_puzzle_hash, coin.amount - fee]
    ]
        
    delegated_puzzle: Program = puzzle_for_conditions(conditions) 
    solution = solution_for_conditions(conditions)

    coin_spend = CoinSpend(
            coin,
            puzzle_reveal,
            solution,
    )
    
    synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
        sk,
        DEFAULT_HIDDEN_PUZZLE_HASH
    )

    sig = AugSchemeMPL.sign(synthetic_sk,
        (
            delegated_puzzle.get_tree_hash()
            + coin.name()
            + bytes.fromhex(keys_utils.genesis_challenge)
        )
    )
    return coin_spend, sig

async def test():
    nft_id = "9caea09e69d68d3f00a624202b24f06049d3b173f76713a327567e308e4790d8"
    nft_coin_info = await get_nft_coin_info(nft_id)
    print(nft_coin_info)

    puzzle_hash = bytes32.from_hexstr("c4766649a0c7c36674ac15bc951aca194d0b92f94e60ecf8160ac6faaff489a7")
    derivation_record = await get_derivation_record_for_puzzle_hash(puzzle_hash)
    print(derivation_record)

    coin_id = bytes32.from_hexstr("15e90f0e8575bdb1c9cb9aadb9144cd435518c906aadc8fc5ac8f4ddc2e8d9b6")
    to_puzzle_hash = bytes32.from_hexstr("0x4a6fffb474f96793ab81616178a02f2089721a1034a04e7ebe5a943075165b23")
    coin_spend, coin_sig = await get_xch_coin_spend_and_signature(coin_id, to_puzzle_hash)
    print(coin_spend)
    print(coin_sig)

asyncio.run(test())
