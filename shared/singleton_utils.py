from typing import List, Tuple

from cdv.test import Wallet

from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.coin import Coin
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
import chia.wallet.puzzles.singleton_top_layer as singleton_top_layer

from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)

import sim
import utils


def create_singleton(wallet: Wallet, start_amount, comment: List[Tuple[str, str]]):
    starting_puzzle: Program = p2_delegated_puzzle_or_hidden_puzzle.puzzle_for_pk(wallet.pk()) # standard tx puzzle
    coin_records = sim.get_coins_records_by_puzzle_hash(starting_puzzle.get_tree_hash())
    starting_coin: Coin = next(cr.coin for cr in coin_records if cr.spent == False)
    assert starting_coin != None

    adapted_puzzle: Program = singleton_top_layer.adapt_inner_to_singleton(starting_puzzle)

    launcher_coin = singleton_top_layer.generate_launcher_coin(starting_coin, start_amount)
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
                start_amount,
                comment,
            ]
        )

    launch_conditions = [
        Program.to(
            [
                ConditionOpcode.CREATE_COIN,
                singleton_top_layer.SINGLETON_LAUNCHER_HASH,
                start_amount,
            ]
        ), 
        Program.to(
            [
                ConditionOpcode.CREATE_COIN,
                starting_puzzle.get_tree_hash(),
                starting_coin.amount - start_amount,
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