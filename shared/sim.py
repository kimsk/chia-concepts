import asyncio
from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)

from cdv.test import Network, Wallet
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.coin_spend import CoinSpend
from chia.types.coin_record import CoinRecord
from chia.types.condition_opcodes import ConditionOpcode
from chia.types.spend_bundle import SpendBundle

from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle,
    singleton_top_layer,
)
network: Network = asyncio.run(Network.create())
asyncio.run(network.farm_block())

alice: Wallet = network.make_wallet("alice")
#print(f'alice pk:\t{alice.pk()}')
bob: Wallet = network.make_wallet("bob")
#print(f'bob pk:\t\t{bob.pk()}')
charlie: Wallet = network.make_wallet("charlie")
#print(f'charlie pk:\t{charlie.pk()}')
dan: Wallet = network.make_wallet("dan")
#print(f'dan pk:\t\t{dan.pk()}')


def farm(farmer: Wallet):
    asyncio.run(network.farm_block(farmer=farmer))

def get_coin(wallet: Wallet, amt, fee=0):
    return asyncio.run(wallet.choose_coin(amt + fee))

def push_tx(spend_bundle: SpendBundle):
    result = asyncio.run(network.push_tx(spend_bundle))
    return result

def launch_smart_coin(wallet: Wallet, puzzle: Program, amt):
    return asyncio.run(wallet.launch_smart_coin(puzzle, amt=amt))

def end():
    asyncio.run(network.close())

def get_coins_records_by_puzzle_hash(puzzle_hash):
    return asyncio.run(network.sim_client.get_coin_records_by_puzzle_hash(puzzle_hash))

def get_coin_record_by_coin_id(coin_id):
    return asyncio.run(network.sim_client.get_coin_record_by_name(coin_id))

def get_coin_records_by_parent_ids(parent_ids):
    return asyncio.run(network.sim_client.get_coin_records_by_parent_ids(parent_ids))

def get_coin_records_by_hint(hint):
    return asyncio.run(network.sim_client.get_coin_record_by_name(hint))

def pass_blocks(number):
    network.sim.pass_blocks(number)

def get_height():
    return network.sim.get_height()

def get_all_non_reward_coins():
    return asyncio.run(network.sim.all_non_reward_coins())

def get_normal_coin_spend(wallet: Wallet, coin, conditions):
    assert coin != None

    delegated_puzzle_solution = Program.to((1, conditions))
    synthetic_sk: PrivateKey = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_secret_key(
        wallet.sk_,
        p2_delegated_puzzle_or_hidden_puzzle.DEFAULT_HIDDEN_PUZZLE_HASH
    )
    synthetic_pk = synthetic_sk.get_g1()

    solution = Program.to([[], delegated_puzzle_solution, []])

    coin_spend = CoinSpend(
            coin.as_coin(),
            wallet.puzzle, # p2_delegated_puzzle_or_hidden_puzzle
            solution,
        )

    sig_msg = delegated_puzzle_solution.get_tree_hash() + coin.name() + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    sig = AugSchemeMPL.sign(synthetic_sk, sig_msg)

    return coin_spend, sig_msg, sig, synthetic_pk

def get_signature(wallet: Wallet, message):
    sk = wallet.sk_
    synthetic_sk: PrivateKey = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_secret_key(
        sk,
        p2_delegated_puzzle_or_hidden_puzzle.DEFAULT_HIDDEN_PUZZLE_HASH
    )
    sig = AugSchemeMPL.sign(synthetic_sk, message)
    return sig