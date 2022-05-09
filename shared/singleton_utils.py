# import sys
# sys.path.insert(0, "../../../shared")
import string
from typing import List, Tuple

from cdv.test import Wallet

from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program, SerializedProgram
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.util.ints import uint64
import chia.wallet.puzzles.singleton_top_layer as singleton_top_layer

from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)

from clvm.casts import int_to_bytes
from clvm_tools.binutils import disassemble

import sim
import utils

START_AMOUNT: uint64 = 1023

def get_singleton(group):
    coin_records = sim.get_coins_records_by_puzzle_hash(singleton_top_layer.SINGLETON_LAUNCHER_HASH) 
    for cr in coin_records:
        coin = cr.coin
        launcher_id = std_hash(
                        coin.parent_coin_info +
                        singleton_top_layer.SINGLETON_LAUNCHER_HASH +
                        int_to_bytes(START_AMOUNT)
        )

        puzz_and_sol = sim.get_puzzle_and_solution(launcher_id, cr.spent_block_index)
        solution: SerializedProgram = puzz_and_sol.solution
        
        solution: Program = solution.to_program()
        # print(disassemble(solution))
        # (0xa1af73b7dc0f246ffb0bd41b4ac8f0253f4c0949bfdd070d52a3be037767baa3 1023 (("Group" . 65)))
        kv = solution.at("rrff")
        # print(disassemble(kv))
        # ("Group" . 67)
        value = kv.as_python()[1].decode('UTF-8')
        # print(value)
        if group == value:
            return coin


def create_singleton(wallet: Wallet, comment: List[Tuple[str, str]]):
    starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet.pk()) # standard tx puzzle
    coin_records: Coin = sim.get_coins_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
    starting_coin: Coin = next(cr.coin for cr in coin_records if cr.spent == False)
    assert starting_coin != None

    adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)

    launcher_coin = singleton_top_layer.generate_launcher_coin(starting_coin, START_AMOUNT)
    launcher_id = launcher_coin.name()
    print(f'launcher_id: {launcher_id}')
    print(f'comment: {comment}')

    # Prepare singleton puzzle using provided singleton_top_layer
    curried_singleton: Program = singleton_top_layer.SINGLETON_MOD.curry(
            (
                singleton_top_layer.SINGLETON_MOD_HASH, 
                (launcher_id, singleton_top_layer.SINGLETON_LAUNCHER_HASH)
            ), # SINGLETON_STRUCT
            adapted_puzzle, # INNER_PUZZLE
        )

    launcher_solution = Program.to(
            [
                curried_singleton.get_tree_hash(),
                START_AMOUNT,
                comment,
            ]
        )

    launch_conditions = [
        Program.to(
            [
                ConditionOpcode.CREATE_COIN,
                singleton_top_layer.SINGLETON_LAUNCHER_HASH,
                START_AMOUNT,
            ]
        ), 
        Program.to(
            [
                ConditionOpcode.CREATE_COIN,
                starting_puzzle.get_tree_hash(),
                starting_coin.amount - START_AMOUNT,
            ]
        ), # changes
        Program.to(
            [
                ConditionOpcode.ASSERT_COIN_ANNOUNCEMENT,
                std_hash(launcher_coin.name() + launcher_solution.get_tree_hash()),
            ]
        )
    ]

    launcher_coin_spend = CoinSpend(
            launcher_coin,
            singleton_top_layer.SINGLETON_LAUNCHER,
            launcher_solution,
        )


    # Creating solution for standard transaction
    delegated_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_conditions(launch_conditions)
    full_solution: Program = p2_delegated_puzzle_or_hidden_puzzle.solution_for_conditions(launch_conditions)

    print(launcher_solution)
    print(full_solution)

    starting_coin_spend = CoinSpend(
        starting_coin, # Alice's
        starting_puzzle, # standard transaction
        full_solution,
    )

    starting_coin_spend_sig = sim.get_signature(
        sim.alice,
        (
            delegated_puzzle.get_tree_hash()
            + starting_coin.name()
            + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
        )
    )

    creating_eve_spend_bundle = SpendBundle(
        [
            starting_coin_spend, 
            launcher_coin_spend
        ],
        starting_coin_spend_sig
    )

    utils.print_json(creating_eve_spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
    return launcher_id, creating_eve_spend_bundle