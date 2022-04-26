import asyncio
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.types.blockchain_format.sized_bytes import bytes32

from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16

# config/config.yaml
config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
selected_network = config["selected_network"]
genesis_challenge = config["farmer"]["network_overrides"]["constants"][selected_network]["GENESIS_CHALLENGE"]
self_hostname = config["self_hostname"] # localhost
wallet_rpc_port = config["wallet"]["rpc_port"] # 9256

async def get_private_key_async(fingerprint: int):
    try:
        wallet_client = await WalletRpcClient.create(
            self_hostname, uint16(wallet_rpc_port), DEFAULT_ROOT_PATH, config
        )
        private_key = await wallet_client.get_private_key(fingerprint)
        return private_key
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

def get_private_key(fingerprint: int):
    return asyncio.run(get_private_key_async(fingerprint))

def get_transaction(tx_id: bytes32):
    return asyncio.run(get_transaction_async(tx_id))