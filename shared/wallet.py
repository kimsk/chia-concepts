import asyncio
from typing import List

from blspy import (PrivateKey, AugSchemeMPL, G1Element)

from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.sized_bytes import bytes32

from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16
from chia.wallet.derive_keys import (
    _derive_path_unhardened
)
from chia.wallet.puzzles import (
    p2_delegated_puzzle_or_hidden_puzzle
)

# config/config.yaml
config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
selected_network = config["selected_network"]
genesis_challenge = config["farmer"]["network_overrides"]["constants"][selected_network]["GENESIS_CHALLENGE"]
self_hostname = config["self_hostname"] # localhost
wallet_rpc_port = config["wallet"]["rpc_port"] # 9256

async def get_private_keys_async(fingerprint: int):
    try:
        wallet_client = await WalletRpcClient.create(
            self_hostname, uint16(wallet_rpc_port), DEFAULT_ROOT_PATH, config
        )
        private_keys = await wallet_client.get_private_key(fingerprint)
        return private_keys
    finally:
        wallet_client.close()
        await wallet_client.await_closed()

async def get_transaction_async(tx_id: bytes32, wallet_id = "1"):
    try:
        wallet_client = await WalletRpcClient.create(
            self_hostname, uint16(wallet_rpc_port), DEFAULT_ROOT_PATH, config
        )
        tx = await wallet_client.get_transaction(wallet_id, tx_id)
        return tx
    finally:
        wallet_client.close()
        await wallet_client.await_closed()

async def get_secret_key_async(fingerprint: int, hd_path: List[int]):
    keys = await get_private_keys_async(fingerprint)
    master_sk: PrivateKey = PrivateKey.from_bytes(bytes.fromhex(keys['sk']))
    sk: PrivateKey = _derive_path_unhardened(master_sk, hd_path)
    return sk

async def get_signature_async(fingerprint: int, 
    hd_path: List[int], 
    message: bytes32):

    sk = await get_secret_key_async(fingerprint, hd_path)
    synthetic_sk: PrivateKey = p2_delegated_puzzle_or_hidden_puzzle.calculate_synthetic_secret_key(
        sk,
        p2_delegated_puzzle_or_hidden_puzzle.DEFAULT_HIDDEN_PUZZLE_HASH
    )
    sig = AugSchemeMPL.sign(synthetic_sk, message)
    return sig

def get_signature(fingerprint: int, 
    hd_path: List[int], 
    message: bytes32): 
    return asyncio.run(get_signature_async(
        fingerprint, 
        hd_path,
        message
    ))

def get_public_key(fingerprint: int, hd_path: List[int]):
    sk = asyncio.run(get_secret_key_async(fingerprint, hd_path))
    return sk.get_g1()

def get_secret_key(fingerprint: int, hd_path: List[int]):
    return asyncio.run(get_secret_key_async(fingerprint, hd_path))

def get_private_keys(fingerprint: int):
    return asyncio.run(get_private_keys_async(fingerprint))

def get_transaction(tx_id: bytes32):
    return asyncio.run(get_transaction_async(tx_id))