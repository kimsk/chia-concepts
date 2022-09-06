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
FINGERPRINT = 1094526214
DB_PATH = Path(f'/Users/karlkim/.chia/testnet10/wallet/db/blockchain_wallet_v2_r1_testnet10_{FINGERPRINT}.sqlite')

async def get_nft_coin_info(nft_id: bytes32):
    query = f"""
        SELECT nft_id, coin, lineage_proof, mint_height, status, full_puzzle, latest_height
        FROM users_nfts WHERE removed_height IS NULL and nft_id='{nft_id.hex()}'
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
    if coin_record == None:
        return None, None

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

# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/wallet.py#L202
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

    # https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/nft_wallet/nft_wallet.py#L600
async def get_nft_coin_spend_and_signature(nft_id: bytes32, buyer_puzzle_hash: bytes32):
    nft_coin_info = await get_nft_coin_info(nft_id)
    if nft_coin_info == None:
        return None, None

    nft_coin = nft_coin_info.coin

    innersol: Program = make_solution(
        primaries = [
            {
                "puzzlehash": buyer_puzzle_hash, 
                "amount": nft_coin.amount, 
                "memos": [buyer_puzzle_hash]
            }
        ]
    )
    
    unft = UncurriedNFT.uncurry(*nft_coin_info.full_puzzle.uncurry())

    # reset DID owner
    # https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/nft_wallet/nft_wallet.py#L715
    new_owner = b""
    new_did_inner_hash = b""
    trade_prices_list = None
    magic_condition = Program.to([-10, new_owner, trade_prices_list, new_did_inner_hash])
    innersol = Program.to([[[], (1, magic_condition.cons(innersol.at("rfr"))), []]])
    
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
            conditions, nft_coin_spend.coin.name(), bytes.fromhex(keys_utils.genesis_challenge)
        ):
            sigs.append(AugSchemeMPL.sign(synthetic_secret_key, msg))
    nft_sig = AugSchemeMPL.aggregate(sigs)
    return nft_coin_spend, nft_sig

async def generate_spend_bundle(
    xch_coin_id,
    acct_puzzle_hash,
    nft_id,
    buyer_puzzle_hash,
    fee = 2_000
):
    xch_coin_spend, xch_sig = await get_xch_coin_spend_and_signature(xch_coin_id, acct_puzzle_hash, fee)
    # print(xch_coin_spend)

    nft_coin_spend, nft_sig = await get_nft_coin_spend_and_signature(nft_id, buyer_puzzle_hash)
    # print(nft_coin_spend)


    agg_sig = AugSchemeMPL.aggregate([xch_sig, nft_sig])
    # print(agg_sig)

    spend_bundle = SpendBundle([
            nft_coin_spend, 
            xch_coin_spend
        ], 
        agg_sig
    )
        
    print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))

async def test_generate_spend_bundle():
    xch_coin_id = bytes32.from_hexstr("057acfb8b9b2fd8452f7c9e9987853ae7ed97186ef919325de9af24584f55435")
    acct_puzzle_hash = bytes32.from_hexstr("9eea4db6c4fde46fc4cdc8adcb7a43d12c60deec352582a84dc550321dc6868c")
    nft_id = bytes32.from_hexstr("73bb7190d270671e5674adca9c3a0e1cda3df4af5aab93a40db4a2fc710e1e4a")
    buyer_puzzle_hash = bytes32.from_hexstr("e8f27d2d5b2fa0faef67eee1840b2ba531a14fad56379b645c947c44f73f6ab8") 

    await generate_spend_bundle(xch_coin_id, acct_puzzle_hash, nft_id, buyer_puzzle_hash)

async def test():
    # nft id (launcher id)
    nft_id = "73bb7190d270671e5674adca9c3a0e1cda3df4af5aab93a40db4a2fc710e1e4a"
    nft_coin_info = await get_nft_coin_info(nft_id)
    print(nft_coin_info)

    puzzle_hash = bytes32.from_hexstr("0x2d1bd7b1bf100d1136d797527c4ff66664f3856a93b529e0f979db7ba302b7c6")
    derivation_record = await get_derivation_record_for_puzzle_hash(puzzle_hash)
    print(derivation_record)

    # coin from buyer
    coin_id = bytes32.from_hexstr("057acfb8b9b2fd8452f7c9e9987853ae7ed97186ef919325de9af24584f55435")
    # destination puzzle hash (accounting)
    to_puzzle_hash = bytes32.from_hexstr("9eea4db6c4fde46fc4cdc8adcb7a43d12c60deec352582a84dc550321dc6868c")
    coin_spend, coin_sig = await get_xch_coin_spend_and_signature(coin_id, to_puzzle_hash)
    print(coin_spend)
    print(coin_sig)

asyncio.run(test_generate_spend_bundle())
