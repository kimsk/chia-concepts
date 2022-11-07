# https://github.com/kimsk/chia-concepts/blob/main/WIP/shared/full_node.py
import asyncio
from typing import List


from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.types.spend_bundle import SpendBundle
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH
from chia.util.ints import uint16

# config/config.yaml
config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
selected_network = config["selected_network"]
genesis_challenge = config["farmer"]["network_overrides"]["constants"][selected_network]["GENESIS_CHALLENGE"]

# print(f'network: {selected_network}')
self_hostname = config["self_hostname"] # localhost
full_node_rpc_port = config["full_node"]["rpc_port"] # 8555

async def get_blockchain_state_async():
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        state = await full_node_client.get_blockchain_state()
        return state
    finally:
        full_node_client.close()
        await full_node_client.await_closed()


async def get_coin_records_by_puzzle_hash_async(puzzle_hash: bytes32):
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        coin_records = await full_node_client.get_coin_records_by_puzzle_hash(puzzle_hash)
        return coin_records
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

async def get_coin_records_by_puzzle_hashes_async(puzzle_hashes: List[bytes32]):
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        coin_records = await full_node_client.get_coin_records_by_puzzle_hashes(puzzle_hashes)
        return coin_records
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

async def get_coin_record_by_name_async(coin_id: bytes32):
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        coin_record = await full_node_client.get_coin_record_by_name(coin_id)
        return coin_record
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

async def get_coin_records_by_parent_ids_async(parent_ids: List[bytes32]):
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        coin_records = await full_node_client.get_coin_records_by_parent_ids(parent_ids)
        return coin_records
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

async def get_coin_records_by_hint_async(hint: bytes32):
    try:
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        coin_records = await full_node_client.get_coin_records_by_hint(hint)
        return coin_records
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

async def push_tx_async(spend_bundle: SpendBundle):
    try:
        # create a full node client
        full_node_client = await FullNodeRpcClient.create(
                self_hostname, uint16(full_node_rpc_port), DEFAULT_ROOT_PATH, config
            )
        status = await full_node_client.push_tx(spend_bundle)
        return status
    finally:
        full_node_client.close()
        await full_node_client.await_closed()

def get_coin_records_by_puzzle_hash(puzzle_hash: bytes32):
    return asyncio.run(get_coin_records_by_puzzle_hash_async(puzzle_hash))

def get_coin_records_by_puzzle_hashes(puzzle_hashes: List[bytes32]):
    return asyncio.run(get_coin_records_by_puzzle_hashes_async(puzzle_hashes))

def get_coin_record_by_name(coin_id: bytes32):
    return asyncio.run(get_coin_record_by_name_async(coin_id))

def get_coin_records_by_parent_ids(parent_ids: List[bytes32]):
    return asyncio.run(get_coin_records_by_parent_ids_async(parent_ids))

def get_coin_records_by_hint(hint: bytes32):
    return asyncio.run(get_coin_records_by_hint_async(hint))

def push_tx(spend_bundle: SpendBundle):
    return asyncio.run(push_tx_async(spend_bundle))