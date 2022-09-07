from blspy import (PrivateKey, AugSchemeMPL,
                   G1Element, G2Element)
                   
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
        DEFAULT_HIDDEN_PUZZLE_HASH, calculate_synthetic_secret_key, puzzle_for_public_key_and_hidden_puzzle_hash
    )

from chia.wallet.puzzles import singleton_top_layer_v1_1
from chia.util.bech32m import decode_puzzle_hash, encode_puzzle_hash

print(singleton_top_layer_v1_1.SINGLETON_MOD_HASH)
exit()

pks = [
    "ac00df28d5916c4a6881c4613a1941ec106a226d9ae78eb20ed65273cee5c83c48ed28c2a8f5b690c2e0b1012027e440",
    "8cea5c2595dfae5623590d3dbd76187da637b8bea8e9b515a95ca1e62096fc411bbfbb55ce3c2c64af9680089275a321",
    "a9f45093d8ea15158f188b1f46a92feefce72719815f2191a19c92b54602a804ad2179659419e72c3e7bfde8df42d5f4",
    "8317ee47021148eab26327227635541cddae6c02735f0ff0e65afc1a36a31206b5c9ffa2cc6ef36e6c9c8fb829e39c5a",
    "879a59ec680527309a21ab6b926d87146933aa5e935ece1165b40d664fe211b7a5292143beb7f4c5ad46932f6e50a2c6",
    "8c1ad7ccb52ac97233c955c9a1bf7d00fee19c502efd2b05e10c693a511e8115d6e719dd5d335e3d1fb657ffd9859a96",
    "a50a113edb58a7bdfcf1392dbb0918bd2c785aafead517e75eda55ffd1a70a7fa6b9a7538a10fdc211afd55629d51882",
    "9918e83891a5afb84a0c944a422e98ed7d47ed9b0688a0db690ab45e35877ebe3d97701fedaef46ff6deadd3852671c0",
    "a2c58dc0b5071f24c94d4a51ca1d19fbceb52723bb2d38b9907b5749e74bbd9ecc483c7e449e9a7fd0f763f17037920a",
    "839cf5c238bdd01a0ab6705530a4430ed0291816d8efa7fc73acfe31248a205722a9a4d05902839e87a1d9f043e58a8"
]

for pk in pks:
    pk_: G1Element = G1Element.from_bytes(bytes.fromhex(pk))

    puzzle = puzzle_for_public_key_and_hidden_puzzle_hash(
        pk_,
        DEFAULT_HIDDEN_PUZZLE_HASH
    )
    puzzhash = puzzle.get_tree_hash()
    txch = encode_puzzle_hash(puzzhash, 'txch')
    print(pk_)
    print(puzzhash)
    print(txch)
    print()