## Prerequisites

### Chia
- [Chia-Blockchain](https://github.com/Chia-Network/chia-blockchain)
- [Chia-Dev-Tools](https://github.com/Chia-Network/chia-dev-tools)

### JupyterLab
- [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html)
```
pip install jupyterlab
```
#### Visualization
- [jupyter-widgets/ipywidgets](https://github.com/jupyter-widgets/ipywidgets)

#### RPC & Sqlite Decorators
- [decorators](https://github.com/kimsk/chia-concepts/blob/main/shared/decorators.py)
- [full_node_rpc](https://github.com/kimsk/chia-concepts/blob/main/shared/full_node_rpc.py)

##### RPC
```python
chia_root = Path('/Users/karlkim/.chia/simulator/dao')
chia_config = load_config(chia_root, "config.yaml")
self_hostname = chia_config["self_hostname"]
full_node_rpc_port = chia_config["full_node"]["rpc_port"]
wallet_rpc_port = chia_config["wallet"]["rpc_port"]

inject_full_node = with_full_node_rpc_client(self_hostname, full_node_rpc_port, chia_root, chia_config)
get_coin_record_by_name = inject_full_node(full_node_rpc.get_coin_record_by_name)
get_coin_records_by_parent_id = inject_full_node(full_node_rpc.get_coin_records_by_parent_id)
get_coin_records_by_puzzle_hash = inject_full_node(full_node_rpc.get_coin_records_by_puzzle_hash)
get_coin_spend = inject_full_node(full_node_rpc.get_coin_spend)
get_coins_in_block = inject_full_node(full_node_rpc.get_coins_in_block)
get_coin_records_by_hint = inject_full_node(full_node_rpc.get_coin_records_by_hint)
```

##### DB
```python
wallet_db = '/Users/karlkim/.chia/testnet10/wallet/db/blockchain_wallet_v2_r1_testnet10_2483575623.sqlite'
@with_db_connection(wallet_db)
async def get_coin_names_by_wallet_id(conn, wallet_id):
    coins = []
    query = "SELECT coin_name FROM coin_record WHERE wallet_id=?"
    async with conn.execute(query, (wallet_id,)) as cursor:
        async for row in cursor:
            coins.append(row[0])
    return coins
await get_coin_names_by_wallet_id(1)
```

### Misc
> PowerShell, C#, and F# Cell supports
- [PowerShell](https://github.com/PowerShell/PowerShell)
- [.NET SDK](https://docs.microsoft.com/en-us/dotnet/core/install/linux-ubuntu)
- [.NET Interactive](https://github.com/dotnet/interactive)

```sh
dotnet tool install Microsoft.dotnet-interactive -g
dotnet interactive jupyter install
```
- [vatlab/jupyterlab-sos](https://github.com/vatlab/jupyterlab-sos)
```
pip install jupyterlab_sos
```
## Notebooks
- [Example](./notebooks/example.ipynb)

### Chialisp
- [Dive into CLVM](notebooks/chialisp/clvm/dive-into-CLVM.ipynb)
- [Map/Reduce/Filter](notebooks/chialisp/map-reduce-filter/notebook.ipynb)
    - [using Lambda](notebooks/chialisp/map-reduce-filter/lambda.ipynb)
- [Modules](notebooks/chialisp/chialisp-modules/notebook.ipynb)

- [apply](notebooks/chialisp/apply/README.md)
- [op_code](notebooks/chialisp/op_code/README.md)
- [quote](notebooks/chialisp/quote/README.md)
- [standard-cl-21](notebooks/chialisp/standard-cl-21/README.md)

### Misc 
- [Automatic Counter](notebooks/misc/counter/README.md)
    - [Normal Coin](notebooks/misc/counter/create-coin.ipynb)
    - [Singleton Counter](notebooks/misc/counter/singleton-counter.ipynb)
- [Tic Tac Toe](notebooks/misc/tic-tac-toe/README.md)

### Basic
- [BLS]
- [Coins](notebooks/basic/coins/notebook.ipynb)
- [Merkel Tree]
- [Outer and Inner Puzzle](/notebooks/basic/outer-and-inner-puzzles/notebook.ipynb)
### Intermediate
- [DIDs](notebooks/intermediate/dids/README.md)
- [Singleton](notebooks/intermediate/singleton/notebook.ipynb)
    - [Singleton Counter (old)](notebooks/intermediate/singleton/singleton_counter.ipynb)
- [Standard Transaction](notebooks/intermediate/standard-transaction/README.md)
- [Pooling]

### Advanced
- [Chia Asset Tokens (CATs)]
- [DataLayer]
- [NFT](notebooks/advanced/nft/README.md)
- [Offers]
