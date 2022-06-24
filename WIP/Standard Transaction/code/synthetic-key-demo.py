import sys
sys.path.insert(0, "../../shared")

from blspy import (AugSchemeMPL, G1Element, PrivateKey)
from cdv.util.load_clvm import load_clvm
from chia.consensus.default_constants import DEFAULT_CONSTANTS
from chia.types.blockchain_format.program import Program
from chia.types.coin_spend import CoinSpend
from chia.types.spend_bundle import SpendBundle
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
    calculate_synthetic_secret_key, 
    calculate_synthetic_public_key)

from sim import alice, bob, farm, get_coin, launch_smart_coin, push_tx, end
from utils import print_json
farm(alice)

password_locked_delegated = load_clvm("password-locked-delegated.clsp", package_or_requirement=__name__, search_paths=["../include"]) 
password_locked_delegated_hash = password_locked_delegated.get_tree_hash()
# 0x5aa1f8e77872fa19b0227e752dee6bafa18b43d37996c4b2a5a845d8959baa2c

synthetic_pk: G1Element = calculate_synthetic_public_key(
    alice.pk(),
    password_locked_delegated_hash
)
print(f'synthetic_pk:\t{synthetic_pk}')

password_locked_puzzle = load_clvm(
        "password-locked-coin.clsp", package_or_requirement=__name__, search_paths=["../include"]
    ).curry(synthetic_pk)
password_locked_puzzle_hash = password_locked_puzzle.get_tree_hash()
print(f'password_locked_coin_hash:\t{password_locked_puzzle_hash}')

amt = 1_000_000_000
password_locked_coin = launch_smart_coin(alice, password_locked_puzzle, amt)
print(password_locked_coin)


# If the solver can correctly reveal BOTH the hidden puzzle and the original public key,
# then our puzzle can derive the synthetic public key 
# and make sure that it matches the one that is curried in.

# (SYNTHETIC_PK original_pk delegated_puzzle solution)
# original_pk is alice's pk (original public key)
# delegated_puzzle is password-locked delegated (hidden puzzle)
# solution is ("hello" bob_puzz_hash amt)
# sending mojos to bob
password_locked_coin_solution = Program.to([
    alice.pk(),
    password_locked_delegated,
    ["hello", bob.puzzle_hash, amt]
])
# print(password_locked_coin_solution)

# use syntheric_sk to sign the spend bundle
# calculate synthetic_sk to sign the spend
synthetic_sk: PrivateKey = calculate_synthetic_secret_key(
    alice.sk_,
    password_locked_delegated_hash
)
sig = AugSchemeMPL.sign(synthetic_sk,
    (
        password_locked_delegated.get_tree_hash()
        + password_locked_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

spend_bundle = SpendBundle(
    [
        CoinSpend(
            password_locked_coin.as_coin(),
            password_locked_puzzle,
            password_locked_coin_solution,
        )
    ],
    sig,
)

result = push_tx(spend_bundle)
print(f'alice balance:\t\t{alice.balance()}')
print(f'bob balance:\t{bob.balance()}')
print_json(spend_bundle.to_json_dict(include_legacy_keys = False, exclude_modern_keys = False))

end()