from typing import List
import json
def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))
    
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.coin_record import CoinRecord
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.util.hash import std_hash
from chia.wallet.puzzles import (singleton_top_layer, p2_delegated_puzzle_or_hidden_puzzle)

from clvm.casts import int_to_bytes

def get_singleton_coin_spend(singleton_coin, singleton_puzzle, lineage_proof, inner_solution):
    singleton_solution = singleton_top_layer.solution_for_singleton(
        lineage_proof,
        singleton_coin.amount,
        inner_solution,
    )

    coin_spend = CoinSpend(
        singleton_coin,
        singleton_puzzle,
        singleton_solution
    )

    return coin_spend

async def get_unspent_singleton(get_coin_records_by_parent_ids, launcher_id):
    parent_coin_id = launcher_id
    while parent_coin_id != None:
        coin_records: List[CoinRecord] = await get_coin_records_by_parent_ids([parent_coin_id], include_spent_coins = True) 
        singleton: CoinRecord = next(cr for cr in coin_records if cr.coin.amount%2 != 0)

        if singleton != None:
            if singleton.spent_block_index == 0:
                return singleton.coin
            parent_coin_id = singleton.coin.name()
        else:
            parent_coin_id = None

def get_create_singleton_coin_spends(
        standard_txn_coin, 
        standard_txn_puzzle,
        odd_amount, inner_puzzle, keys_values
    ):
    assert standard_txn_coin.amount >= odd_amount

    launcher_coin = Coin(
        standard_txn_coin.name(), 
        singleton_top_layer.SINGLETON_LAUNCHER_HASH, 
        odd_amount
    )
    launcher_id = launcher_coin.name()

    singleton_struct = (
        singleton_top_layer.SINGLETON_MOD_HASH, 
        (launcher_id, singleton_top_layer.SINGLETON_LAUNCHER_HASH)
    )
    curried_singleton_puzzle = singleton_top_layer.SINGLETON_MOD.curry(
            singleton_struct,
            inner_puzzle,
    )
    singleton_puzzle_hash = curried_singleton_puzzle.get_tree_hash()

    launcher_solution = Program.to(
        [
            singleton_puzzle_hash,
            int_to_bytes(odd_amount),
            keys_values,
        ]
    )

    launcher_coin_spend = CoinSpend(
            launcher_coin,
            singleton_top_layer.SINGLETON_LAUNCHER,
            launcher_solution
    )
    launcher_announcement = launcher_solution.get_tree_hash()
    standard_txn_coin_conditions = [
        # create launcher coin with the odd_amount (odd)
        Program.to(
            [
                ConditionOpcode.CREATE_COIN,
                singleton_top_layer.SINGLETON_LAUNCHER_HASH,
                odd_amount,
            ]),
        # assert launcher coin announcement
        Program.to(
            [
                ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT, 
                std_hash(launcher_id + launcher_announcement)
            ]),
    ]
    if standard_txn_coin.amount > odd_amount:
        standard_txn_coin_conditions = [
            *standard_txn_coin_conditions, 
            Program.to(
            [
                ConditionOpcode.CREATE_COIN,
                standard_txn_coin.puzzle_hash,
                standard_txn_coin.amount - odd_amount,
            ])
        ]

        
    delegated_puzzle = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_conditions(standard_txn_coin_conditions)
    solution = p2_delegated_puzzle_or_hidden_puzzle.solution_for_conditions(standard_txn_coin_conditions)
    
    standard_txn_coin_spend = CoinSpend(
        standard_txn_coin,
        standard_txn_puzzle,
        solution
    )
    
    standard_coin_message = (
        delegated_puzzle.get_tree_hash()
        + standard_txn_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
    return standard_coin_message, [standard_txn_coin_spend, launcher_coin_spend]