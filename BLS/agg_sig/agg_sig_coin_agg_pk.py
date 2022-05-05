import asyncio
import json

from blspy import (PrivateKey, AugSchemeMPL, G2Element)
from cdv.test import Network, Wallet
from cdv.util.load_clvm import load_clvm
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.spend_bundle import SpendBundle
from chia.util.hash import std_hash

from chia.util.ints import uint64
from clvm.casts import int_to_bytes

def print_json(dict):
    print(json.dumps(dict, sort_keys=True, indent=4))

network: Network = asyncio.run(Network.create())
asyncio.run(network.farm_block())
alice: Wallet = network.make_wallet("alice")
bob: Wallet = network.make_wallet("bob")
owner1: Wallet = network.make_wallet("owner1")
owner2: Wallet = network.make_wallet("owner2")
owner3: Wallet = network.make_wallet("owner3")
asyncio.run(network.farm_block(farmer=alice))
# print(len(alice.usable_coins))
# print(alice.balance())


AGG_SIG_COIN = load_clvm("agg_sig_coin_agg_pk.clsp", package_or_requirement=__name__, search_paths=["../include"])
# print(AGG_SIG_COIN.get_tree_hash())

amt = 1000000000000
agg_sig_coin = asyncio.run(alice.launch_smart_coin(AGG_SIG_COIN, amt=amt))
# print(agg_sig_coin.as_coin())

agg_pk = owner1.pk() + owner2.pk() + owner3.pk()

agg_sig_coin_solution = Program.to([amt, bob.puzzle_hash, agg_pk])

spend = CoinSpend(
    agg_sig_coin.as_coin(),
    AGG_SIG_COIN,
    agg_sig_coin_solution 
)

sk1: PrivateKey = owner1.pk_to_sk(owner1.pk())
sk2: PrivateKey = owner2.pk_to_sk(owner2.pk())
sk3: PrivateKey = owner3.pk_to_sk(owner3.pk())
message: bytes = std_hash(int_to_bytes(agg_sig_coin.amount))
sig1: G2Element = AugSchemeMPL.sign(sk1,
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    agg_pk
                )

sig2: G2Element = AugSchemeMPL.sign(sk2,
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    agg_pk
                )

sig3: G2Element = AugSchemeMPL.sign(sk3,
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    agg_pk
                )
agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])

assert AugSchemeMPL.verify(agg_pk,
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    agg_sig)

assert AugSchemeMPL.aggregate_verify([agg_pk],
                    [
                        message
                        + agg_sig_coin.name()
                        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
                    ],
                    agg_sig)


spend_bundle = SpendBundle([spend], agg_sig)
# print(spend_bundle)

#print(bob.balance())
asyncio.run(network.push_tx(spend_bundle))
# asyncio.run(network.farm_block())

#print(bob.balance())
coin_records = asyncio.run(network.sim_client.get_coin_records_by_puzzle_hash((AGG_SIG_COIN.get_tree_hash())))
#print(coin_records)
asyncio.run(network.close())

print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
