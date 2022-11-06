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
from chia.util.condition_tools import conditions_dict_for_solution, pkm_pairs_for_conditions_dict
from chia.util.db_wrapper import DBWrapper2, execute_fetchone
from chia.util.ints import uint32
from chia.wallet.derivation_record import DerivationRecord
from chia.wallet.lineage_proof import LineageProof
from chia.wallet.nft_wallet.nft_info import IN_TRANSACTION_STATUS, NFTCoinInfo, NFTWalletInfo
from chia.wallet.util.wallet_types import AmountWithPuzzlehash, WalletType
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

from chia.wallet.nft_wallet.uncurry_nft import UncurriedNFT
from chia.types.coin_spend import CoinSpend
from chia.types.spend_bundle import SpendBundle
from chia.types.condition_opcodes import ConditionOpcode


def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))



DB_VERSION = 2
FINGERPRINT = 1094526214
DB_PATH = Path(f'/Users/karlkim/.chia/testnet10/wallet/db/blockchain_wallet_v2_r1_testnet10_{FINGERPRINT}.sqlite')
# FINGERPRINT = 4096957589
# DB_PATH = Path(f'/mnt/e/testnet/wallet/db/blockchain_wallet_v2_r1_testnet10_{FINGERPRINT}.sqlite')

async def get_derivation_record_for_puzzle_hash(puzzle_hash: bytes32):
    try:
        connection = await aiosqlite.connect(DB_PATH)
        db_wrapper = DBWrapper2(connection, DB_VERSION)
        read_connection = await aiosqlite.connect(DB_PATH)

        await db_wrapper.add_connection(read_connection)

        async with db_wrapper.reader_no_transaction() as conn:
            row = await execute_fetchone(
                conn,
                "SELECT derivation_index, pubkey, puzzle_hash, wallet_type, wallet_id, hardened "
                "FROM derivation_paths "
                "WHERE puzzle_hash=?",
                (puzzle_hash.hex(),),
            )

        if row is not None and row[0] is not None:
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
    finally: 
        await db_wrapper.close()
    
async def keys_for_puzzle_hash(puzzle_hash: bytes32):
    derivation_record = await get_derivation_record_for_puzzle_hash(puzzle_hash)
    
    if derivation_record is not None:
        # wallet hd-path (m/12381/8444/2/{idx})
        hd_path = [12381, 8444, 2, derivation_record.index]
        sk = await keys_utils.get_secret_key_async(FINGERPRINT, hd_path)
        pk = sk.get_g1()
        return sk, pk 

    return None, None

async def get_nft_coin_info(nft_id):
    try:
        connection = await aiosqlite.connect(DB_PATH)
        db_wrapper = DBWrapper2(connection, DB_VERSION)
        read_connection = await aiosqlite.connect(DB_PATH)

        await db_wrapper.add_connection(read_connection)

        async with db_wrapper.reader_no_transaction() as conn:
            row = await execute_fetchone(
                conn,
                "SELECT nft_id, coin, lineage_proof, mint_height, status, full_puzzle, latest_height"
                " from users_nfts WHERE removed_height is NULL and nft_id=?",
                (nft_id,),
            )

        if row is not None and row[0] is not None:
            full_puzzle = Program.from_bytes(row[5])
            nft_coin_info = NFTCoinInfo(
                    bytes32.from_hexstr(row[0]),
                    Coin.from_json_dict(json.loads(row[1])),
                    None if row[2] is None else LineageProof.from_json_dict(json.loads(row[2])),
                    full_puzzle,
                    uint32(row[3]),
                    uint32(row[6]) if row[6] is not None else uint32(0),
                    row[4] == IN_TRANSACTION_STATUS,
            )            
            return nft_coin_info

        return None
    finally: 
        await db_wrapper.close()

async def get_xch_coin_spend_with_signature(coin_id: bytes32):
    coin_record = await full_node.get_coin_record_by_name_async(coin_id)
    coin = coin_record.coin
    sk, pk = await keys_for_puzzle_hash(coin.puzzle_hash)
    # print(coin_record)
    # print(sk)
    # print(pk)

    fee = 2_000

    puzzle_reveal = puzzle_for_pk(pk)
    conditions = [
        [ConditionOpcode.CREATE_COIN, coin.puzzle_hash, coin.amount - fee]
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

def make_solution(
    primaries: List[AmountWithPuzzlehash]
) -> Program:
    condition_list = []
    if len(primaries) > 0:
        for primary in primaries:
            if "memos" in primary:
                memos: Optional[List[bytes]] = primary["memos"]
                if memos is not None and len(memos) == 0:
                    memos = None
            else:
                memos = None
            condition_list.append(make_create_coin_condition(primary["puzzlehash"], primary["amount"], memos))
    return solution_for_conditions(condition_list)

# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/rpc/wallet_rpc_api.py#L1593
    # txs = await nft_wallet.generate_signed_transaction(
    #     [uint64(nft_coin_info.coin.amount)],
    #     [puzzle_hash],
    #     coins={nft_coin_info.coin},
    #     fee=fee,
    #     new_owner=b"",
    #     new_did_inner_hash=b"",
    # )

async def main():
    # coin_id = bytes32.from_hexstr("0x7a30d41e520f7ff00ca88d8875d3d81ff9bff301b67c6cf2e9a4054d7f32618c")
    coin_id = bytes32.from_hexstr("0x7a30d41e520f7ff00ca88d8875d3d81ff9bff301b67c6cf2e9a4054d7f32618c") 
    coin_spend, coin_sig = await get_xch_coin_spend_with_signature(coin_id)

    # coin_spend_bundle = SpendBundle([coin_spend], coin_sig)
    # print_json(coin_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))    
    # exit()
    # nft_id = "8a5ffd6a6e33d3e095ea0338dbb0c5331be6ebc257d50e07e06f68c5692a29bf"
    # nft_id = "9caea09e69d68d3f00a624202b24f06049d3b173f76713a327567e308e4790d8" # without DID

    # nft_id = "c46983b231c50c2e863fd7e1511f4723e502a1a5d80e432154df48ea79566a5e" # with DID
    # nft_id = "5d9858cb9ed67dbd1e8d72b249da1bfac6438c0aa29a794d6e4f9638cd1f4258" # with DID
    # nft_id = "aa91bb6bcec90b2fd34247a324ef66d80a84f2926d184dcad694f7fc1104bcf6" # with DID, MBA
    nft_id = "73bb7190d270671e5674adca9c3a0e1cda3df4af5aab93a40db4a2fc710e1e4a" # with DID, MBA

    # https://github.com/Chia-Network/chia-blockchain/blob/main/chia/rpc/wallet_rpc_api.py#L1609
    
    # txch1yw7a8qxzx0zsvrwgdenl9s8mtdlpgnjsramz5mtcd4nymz87szlqpcxdca
    # to_puzzle_hash = bytes32.from_hexstr("0x23bdd380c233c5060dc86e67f2c0fb5b7e144e501f762a6d786d664d88fe80be")

    # txch1wguv57xlcfc9r02lxf0nkw7332l6pq24wy8c2gf8rymw9z8005gq5sy5ss
    # to_puzzle_hash = bytes32.from_hexstr("0x7238ca78dfc27051bd5f325f3b3bd18abfa08155710f8521271936e288ef7d10")

    # txch14dt7eugam2jlkfz6qnd7735fuygqz8uyytwaqpdaqeuql5az0h7s7pf6w8
    to_puzzle_hash = bytes32.from_hexstr("0xe8f27d2d5b2fa0faef67eee1840b2ba531a14fad56379b645c947c44f73f6ab8")

    nft_coin_info = await get_nft_coin_info(nft_id)
    #print(nft_coin_info)
    if nft_coin_info == None:
        exit(1)

    nft_coin = nft_coin_info.coin

    # https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/nft_wallet/nft_wallet.py#L600

    primaries: List = []
    primaries.append({"puzzlehash": to_puzzle_hash, "amount": nft_coin.amount, "memos": [to_puzzle_hash]})

    innersol: Program = make_solution(
        primaries=primaries
    )

    unft = UncurriedNFT.uncurry(*nft_coin_info.full_puzzle.uncurry())

    # reset DID owner
    # https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/nft_wallet/nft_wallet.py#L715
    new_owner = b""
    new_did_inner_hash = b""
    trade_prices_list = None
    magic_condition = Program.to([-10, new_owner, trade_prices_list, new_did_inner_hash])
    innersol = Program.to([[], (1, magic_condition.cons(innersol.at("rfr"))), []])
    innersol = Program.to([innersol])

    nft_layer_solution = Program.to([innersol])
    singleton_solution = Program.to([nft_coin_info.lineage_proof.to_program(), nft_coin.amount, nft_layer_solution])
    nft_coin_spend = CoinSpend(nft_coin, nft_coin_info.full_puzzle, singleton_solution)

    # get the valid signature
    uncurried_nft = UncurriedNFT.uncurry(*nft_coin_spend.puzzle_reveal.to_program().uncurry())
    ph = uncurried_nft.p2_puzzle.get_tree_hash()
    sk, pk = await keys_for_puzzle_hash(ph)

    synthetic_secret_key = calculate_synthetic_secret_key(sk, DEFAULT_HIDDEN_PUZZLE_HASH)
    synthetic_pk = synthetic_secret_key.get_g1()

    error, conditions, cost = conditions_dict_for_solution(
        nft_coin_spend.puzzle_reveal.to_program(),
        nft_coin_spend.solution.to_program(),
        DEFAULT_CONSTANTS.MAX_BLOCK_COST_CLVM,
    )

    sigs = [coin_sig]
    if conditions is not None:
        for pk, msg in pkm_pairs_for_conditions_dict(
            conditions, nft_coin_spend.coin.name(), bytes.fromhex(keys_utils.genesis_challenge)
        ):
            sigs.append(AugSchemeMPL.sign(synthetic_secret_key, msg))

    agg_sig = AugSchemeMPL.aggregate(sigs)

    nft_spend_bundle = SpendBundle([nft_coin_spend, coin_spend], agg_sig)
    print_json(nft_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))

asyncio.run(main())
