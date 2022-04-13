# https://docs.chia.net/docs/09keys/keys-and-signatures
# https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/derive_keys.py
from blspy import (AugSchemeMPL, G1Element, G2Element, PrivateKey)
from chia.wallet.derive_keys import (
    master_sk_to_farmer_sk,
    master_sk_to_pool_sk,
    master_sk_to_wallet_sk,
    find_authentication_sk,
    find_owner_sk,
    _derive_path
)
from cdv.util.keys import private_key_for_index

master_sk: PrivateKey = private_key_for_index(0)
wallet_sk_0: PrivateKey = master_sk_to_wallet_sk(master_sk, 0)

wallet_hd_path = [12381, 8444, 2, 0]
wallet_sk_path_0 = _derive_path(master_sk, wallet_hd_path)

print(wallet_sk_0)
print(wallet_sk_path_0)

wallet_sk_path_1 = _derive_path(wallet_sk_path_0, [1])
print(wallet_sk_path_1)
wallet_sk_path_2 = _derive_path(wallet_sk_path_0, [2])
print(wallet_sk_path_2)