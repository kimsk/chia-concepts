import aiosqlite
import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import sys
sys.path.insert(0, ".")
import keys_utils
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

def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))


DB_VERSION = 2
# DB_PATH = Path('/Users/karlkim/.chia/testnet10/wallet/db/blockchain_wallet_v2_r1_testnet10_3690011039.sqlite')
FINGERPRINT = 4096957589
DB_PATH = Path(f'/mnt/e/testnet/wallet/db/blockchain_wallet_v2_r1_testnet10_{FINGERPRINT}.sqlite')

async def keys_for_puzzle_hash(puzzle_hash: bytes32):
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

            # wallet hd-path (m/12381/8444/2/{idx})
            hd_path = [12381, 8444, 2, derivation_record.index]
            sk = await keys_utils.get_secret_key_async(FINGERPRINT, hd_path)
            pk = sk.get_g1()
            return sk, pk 

        return None
    finally: 
        await db_wrapper.close()

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

def make_solution(
    primaries: List[AmountWithPuzzlehash],
    min_time=0,
    me=None,
    coin_announcements: Optional[Set[bytes]] = None,
    coin_announcements_to_assert: Optional[Set[bytes32]] = None,
    puzzle_announcements: Optional[Set[bytes]] = None,
    puzzle_announcements_to_assert: Optional[Set[bytes32]] = None,
    fee=0,
) -> Program:
    assert fee >= 0
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
    if min_time > 0:
        condition_list.append(make_assert_absolute_seconds_exceeds_condition(min_time))
    if me:
        condition_list.append(make_assert_my_coin_id_condition(me["id"]))
    if fee:
        condition_list.append(make_reserve_fee_condition(fee))
    if coin_announcements:
        for announcement in coin_announcements:
            condition_list.append(make_create_coin_announcement(announcement))
    if coin_announcements_to_assert:
        for announcement_hash in coin_announcements_to_assert:
            condition_list.append(make_assert_coin_announcement(announcement_hash))
    if puzzle_announcements:
        for announcement in puzzle_announcements:
            condition_list.append(make_create_puzzle_announcement(announcement))
    if puzzle_announcements_to_assert:
        for announcement_hash in puzzle_announcements_to_assert:
            condition_list.append(make_assert_puzzle_announcement(announcement_hash))
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
    # nft_id = "8a5ffd6a6e33d3e095ea0338dbb0c5331be6ebc257d50e07e06f68c5692a29bf"
    nft_id = "9caea09e69d68d3f00a624202b24f06049d3b173f76713a327567e308e4790d8"
    # txch1yw7a8qxzx0zsvrwgdenl9s8mtdlpgnjsramz5mtcd4nymz87szlqpcxdca
    to_puzzle_hash = bytes32.from_hexstr("0x23bdd380c233c5060dc86e67f2c0fb5b7e144e501f762a6d786d664d88fe80be")
    nft_coin_info = await get_nft_coin_info(nft_id)
    #print(nft_coin_info)
    if nft_coin_info == None:
        exit(1)

    nft_coin = nft_coin_info.coin

    # https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/nft_wallet/nft_wallet.py#L600

    primaries: List = []
    primaries.append({"puzzlehash": to_puzzle_hash, "amount": nft_coin.amount, "memos": [to_puzzle_hash]})
            
    coin_announcements_bytes = None
    puzzle_announcements_bytes = None

    # FEE COIN
    # if fee > 0:
    #     announcement_to_make = nft_coin.coin.name()
    #     chia_tx = await self.create_tandem_xch_tx(fee, Announcement(nft_coin.coin.name(), announcement_to_make))
    # else:
    #     announcement_to_make = None
    #     chia_tx = None
    announcement_to_make = None

    innersol: Program = make_solution(
        primaries=primaries,
        coin_announcements=None if announcement_to_make is None else set((announcement_to_make,)),
        coin_announcements_to_assert=coin_announcements_bytes,
        puzzle_announcements_to_assert=puzzle_announcements_bytes,
    )

    unft = UncurriedNFT.uncurry(*nft_coin_info.full_puzzle.uncurry())
    if unft.supports_did:
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

    sigs = []
    if conditions is not None:
        for pk, msg in pkm_pairs_for_conditions_dict(
            conditions, nft_coin_spend.coin.name(), DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
        ):
            sigs.append(AugSchemeMPL.sign(synthetic_secret_key, msg))

    agg_sig = AugSchemeMPL.aggregate(sigs)

    nft_spend_bundle = SpendBundle([nft_coin_spend], agg_sig)

    print_json(nft_spend_bundle.to_json_dict())

asyncio.run(main())
