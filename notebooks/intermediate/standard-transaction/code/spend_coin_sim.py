import sys
sys.path.insert(0, "../../shared")

import asyncio

import utils

from blspy import (PrivateKey, AugSchemeMPL, G2Element)
from cdv.test import Network, SmartCoinWrapper, Wallet
from cdv.util.load_clvm import load_clvm
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import DEFAULT_HIDDEN_PUZZLE_HASH, calculate_synthetic_secret_key, puzzle_for_public_key_and_hidden_puzzle_hash

network: Network = asyncio.run(Network.create())
asyncio.run(network.farm_block())

alice: Wallet = network.make_wallet("alice")
bob: Wallet = network.make_wallet("bob")

asyncio.run(network.farm_block(farmer=alice))
print(f'alice balance:\t{alice.balance()}')
print(f'bob balance:\t{bob.balance()}')

alice_coins = alice.usable_coins 
print(f'alice coins:')
for k, c in alice_coins.items():
    print(k)
    utils.print_json(c.to_json_dict())

# spend standard transaction coin
# alice sends 1 million mojos to bob
amt = 1_000_000
alice_coin = asyncio.run(alice.choose_coin(amt))
assert alice_coin != None
print(f'alice coin:\t{alice_coin}')

# conditions provided by wallet
condition_args = [
    [ConditionOpcode.CREATE_COIN, bob.puzzle_hash, amt],
    [ConditionOpcode.CREATE_COIN, alice.puzzle_hash, alice_coin.amount - amt],
]

delegated_puzzle_solution = Program.to((1, condition_args))

# calculate synthetic_sk to sign the spend
synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
    alice.sk_,
    DEFAULT_HIDDEN_PUZZLE_HASH
)

# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.clvm
# (synthetic_public_key original_public_key delegated_puzzle solution)
# synthetic_public_key is curried in
# original_public_key is ()
# delegated_puzzle is (1 (CREATE_COIN bob amt) (CREATE_COIN alice change))
# solution is ()
solution = Program.to([[], delegated_puzzle_solution, []])

# coins can be unlocked by signing a delegated puzzle and its solution
sig = AugSchemeMPL.sign(synthetic_sk,
    (
        delegated_puzzle_solution.get_tree_hash()
        + alice_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

alice_puzzle = puzzle_for_public_key_and_hidden_puzzle_hash(
    alice.pk(), DEFAULT_HIDDEN_PUZZLE_HASH
)
print(f'alice puzzle: {alice_puzzle}')

# all puzzle hashes have to be the same
print(f'alice_puzzle_hash:\t{alice_puzzle.get_tree_hash()}')
print(f'alice.puzzle_hash:\t{alice.puzzle.get_tree_hash()}')
print(f'alice_coin.puzzle_hash:\t{alice_coin.puzzle_hash}')
assert alice_puzzle.get_tree_hash() == alice_coin.puzzle_hash
assert alice.puzzle.get_tree_hash() == alice_coin.puzzle_hash


spend_bundle = SpendBundle(
    [
        CoinSpend(
            alice_coin.as_coin(),
            alice.puzzle, # p2_delegated_puzzle_or_hidden_puzzle
            solution,
        )
    ],
    sig,
)

asyncio.run(network.push_tx(spend_bundle))
print(f'alice balance:\t{alice.balance()}')
print(f'bob balance:\t{bob.balance()}')

alice_coin_id = alice_coin.name()
alice_coin_record = asyncio.run(
    network.sim_client.get_coin_record_by_name(alice_coin_id))
print(alice_coin_record)

coin_spend: CoinSpend = asyncio.run(
    network.sim_client.get_puzzle_and_solution(alice_coin_id, alice_coin_record.spent_block_index))
print(coin_spend.puzzle_reveal)
print(alice_puzzle)
print(coin_spend.solution)

assert alice_puzzle.get_tree_hash() == coin_spend.puzzle_reveal.get_tree_hash()

asyncio.run(network.close())
