import aiosqlite
from pathlib import Path

from chia.rpc.full_node_rpc_client import FullNodeRpcClient
from chia.rpc.wallet_rpc_client import WalletRpcClient

# decorator
# https://medium.com/opex-analytics/database-connections-in-python-extensible-reusable-and-secure-56ebcf9c67fe
# https://blog.miguelgrinberg.com/post/the-ultimate-guide-to-python-decorators-part-iii-decorators-with-arguments

def with_db_connection(db):
    db_path = Path(db)
    def _with_db_connection(f):
        async def with_connection(*args, **kwargs):
            conn = await aiosqlite.connect(db_path)
            try:
                rv = await f(conn, *args, **kwargs)
            except Exception:
                await conn.rollback()
                raise
            else:
                await conn.commit()
            finally:
                await conn.close()

            return rv

        return with_connection
    return _with_db_connection

async def run_rpc(rpc_client, f, *args, **kwargs):
    try:
        result = await f(rpc_client, *args, **kwargs)
    except Exception:
        raise
    finally:
        rpc_client.close()
        await rpc_client.await_closed()
    return result

def with_full_node_rpc_client(
        self_hostname,
        rpc_port,
        chia_root,
        chia_config):
    def _with_full_node_rpc_client(f):
        async def with_rpc_client(*args, **kwargs):
            rpc_client = await FullNodeRpcClient.create(
                self_hostname, rpc_port, chia_root, chia_config
            )
            return await run_rpc(rpc_client, f, *args, **kwargs)

        return with_rpc_client
    return _with_full_node_rpc_client

def with_wallet_rpc_client(
        self_hostname,
        rpc_port,
        chia_root,
        chia_config):
    def _with_wallet_rpc_client(f):
        async def with_rpc_client(*args, **kwargs):
            rpc_client = await WalletRpcClient.create(
                self_hostname, rpc_port, chia_root, chia_config
            )
            return await run_rpc(rpc_client, f, *args, **kwargs)

        return with_rpc_client
    return _with_wallet_rpc_client