import asyncio
import json
from typing import List

from blspy import (PrivateKey, AugSchemeMPL, G1Element, G2Element)
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
pk1: G1Element = owner1.pk() 
pk2: G1Element = owner2.pk()
pk3: G1Element = owner3.pk()

keys: List[G1Element] = [owner1.pk(), owner2.pk(), owner3.pk()]

sk1: PrivateKey = owner1.pk_to_sk(owner1.pk())
sk2: PrivateKey = owner2.pk_to_sk(owner2.pk())
sk3: PrivateKey = owner3.pk_to_sk(owner3.pk())

asyncio.run(network.farm_block(farmer=alice))

AGG_SIG_COIN = load_clvm("agg_sig_coin_pks.clsp", package_or_requirement=__name__, search_paths=["../include"])

amt = 1000000000000
agg_sig_coin = asyncio.run(alice.launch_smart_coin(AGG_SIG_COIN, amt=amt))

agg_sig_coin_solution = Program.to([amt, bob.puzzle_hash, keys])

spend = CoinSpend(
    agg_sig_coin.as_coin(),
    AGG_SIG_COIN,
    agg_sig_coin_solution 
)

# print(agg_sig_coin.amount)
message: bytes = std_hash(int_to_bytes(agg_sig_coin.amount))
# print(str(message))
sig1: G2Element = AugSchemeMPL.sign(sk1,
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
                )

sig2: G2Element = AugSchemeMPL.sign(sk2,
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
                )

sig3: G2Element = AugSchemeMPL.sign(sk3,
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
                )

assert AugSchemeMPL.verify(owner1.pk(),
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    sig1)
assert AugSchemeMPL.verify(owner2.pk(),
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    sig2)
assert AugSchemeMPL.verify(owner3.pk(),
                    message
                    + agg_sig_coin.name()
                    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    sig3)

agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])

assert AugSchemeMPL.aggregate_verify(
                [owner1.pk(), owner2.pk(), owner3.pk()],
                [
                    message + agg_sig_coin.name() + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    message + agg_sig_coin.name() + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
                    message + agg_sig_coin.name() + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
                ],
                agg_sig)

spend_bundle = SpendBundle([spend], agg_sig)

# print(bob.balance())
asyncio.run(network.push_tx(spend_bundle))
# print(bob.balance())

asyncio.run(network.close())

print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))
