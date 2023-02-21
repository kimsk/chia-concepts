from chia.types.blockchain_format.sized_bytes import bytes32

# use with @with_full_node_rpc_client(self_hostname, full_node_rpc_port, chia_root, chia_config)
async def get_coin_record_by_name(full_node_client, name: bytes32):
    coin_records = await full_node_client.get_coin_record_by_name(
        name
    )
    return coin_records

async def get_coin_records_by_parent_id(full_node_client, parent_id: bytes32):
    coin_records = await full_node_client.get_coin_records_by_parent_ids(
        [parent_id]
    )
    return coin_records

async def get_coin_records_by_puzzle_hash(full_node_client, puzzle_hash: bytes32):
    coin_records = await full_node_client.get_coin_records_by_puzzle_hash(
        puzzle_hash
    )
    return coin_records

async def get_coin_records_by_hint(full_node_client, hint: bytes32):
    coin_records = await full_node_client.get_coin_records_by_hint(
        hint
    )
    return coin_records

async def get_coin_spend(full_node_client, coin_id: bytes32, spent_height):
    coin_spend = await full_node_client.get_puzzle_and_solution(coin_id, spent_height)
    return coin_spend

async def get_coins_in_block(full_node_client, height):
    block_records = await full_node_client.get_block_records(height, height + 1)
    header_hash = bytes32.from_hexstr(block_records[0]['header_hash'])
    result = await full_node_client.get_additions_and_removals(header_hash)
    return result
