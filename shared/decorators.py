import aiosqlite
from pathlib import Path

from chia.rpc.full_node_rpc_client import FullNodeRpcClient

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
