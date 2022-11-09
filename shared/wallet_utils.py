from blspy import (PrivateKey, G1Element)

from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.wallet.derive_keys import (
    _derive_path_unhardened
)
from chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle import (
    calculate_synthetic_public_key,
    calculate_synthetic_secret_key,
    DEFAULT_HIDDEN_PUZZLE_HASH
)
# wallet hd-path (m/12381/8444/2/{idx})
wallet_hd_path = [12381, 8444, 2]

def get_secret_key(master_sk, hd_path):
    return _derive_path_unhardened(master_sk, hd_path)

async def get_master_secret_key(wallet_client: WalletRpcClient, fingerprint):
    keys = await wallet_client.get_private_key(fingerprint)
    return PrivateKey.from_bytes(bytes.fromhex(keys['sk']))

async def get_wallet_secret_keys(wallet_client: WalletRpcClient, fingerprint, n = 0):
    master_sk: PrivateKey = await get_master_secret_key(wallet_client, fingerprint)

    secret_keys = []
    for i in range(n+1):
        hd_path = wallet_hd_path + [i]
        sk: PrivateKey = get_secret_key(master_sk, hd_path) 
        secret_keys.append(sk)
    return secret_keys

async def get_wallet_public_keys(wallet_client: WalletRpcClient, fingerprint, n = 0):
    secret_keys = await get_wallet_secret_keys(wallet_client, fingerprint, n)
    return list(map(lambda sk: sk.get_g1(), secret_keys))

async def get_synthetic_public_keys(wallet_client: WalletRpcClient, fingerprint, n = 0):
    public_keys = await get_wallet_public_keys(wallet_client, fingerprint, n)
    return list(map(lambda pk: calculate_synthetic_public_key(pk, DEFAULT_HIDDEN_PUZZLE_HASH), public_keys))

async def synthetic_pk_to_sk(wallet_client: WalletRpcClient, fingerprint, synthetic_pk: G1Element, n = 0):
    try:
        synthetic_public_keys = await get_synthetic_public_keys(wallet_client, fingerprint, n)
        hd_path = wallet_hd_path + [synthetic_public_keys.index(synthetic_pk)]
        master_sk: PrivateKey = await get_master_secret_key(wallet_client, fingerprint)
        return calculate_synthetic_secret_key(
                get_secret_key(master_sk, hd_path), 
                DEFAULT_HIDDEN_PUZZLE_HASH
        )
    except:
        return None
