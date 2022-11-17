## [Hinting](https://docs.chia.net/conditions#hinting)
> A hint is another word for memo. It's an extra value linked to coins that gets indexed by full nodes. Given a hint, a wallet can discover all coins which include that hint. Additionally, once a wallet has found a coin that includes a hint, it will have another piece of information to determine how it should be spent.

### How To Find Hint?
> Typically, a hint is the coin's inner puzzle hash. When a wallet sees a hint, it fetches the parent coin spend and attempts to use the hint to figure out the coin's type.

#### [DID](../../intermediate/dids/DID-hints.ipynb)
Hint is the wallet puzzle hash.
```sh
❯ chia keys derive -f $alice_fp wallet-address -n 2 |
∙ select -Skip 1 -First 1 |
∙ % { cdv decode $_.SubString($_.Length - 63, 63) } |
∙ % { chia rpc full_node get_coin_records_by_hint (@{ hint = $_ } | ConvertTo-Json) }
{
    "coin_records": [
        {
            "coin": {
                "amount": 1,
                "parent_coin_info": "0x8623b84e3a51821925524049d99c0ec658c10da85ac442c7c2f66d17e737abed",
                "puzzle_hash": "0xd184baf53ae672f90423dd9427b52a052770471e167e6dc9e84dde062c3b7b38"
            },
            "coinbase": false,
            "confirmed_block_index": 5,
            "spent": false,
            "spent_block_index": 0,
            "timestamp": 1668527771
        }
    ],
    "success": true
}
```

#### NFT
#### CAT


### Get Coin By Hint
- [/get_coin_records_by_hint](https://docs.chia.net/full-node-rpc#get_coin_records_by_hint)
- [get coin id from wallet db](../../misc/sqlite/hints.ipynb)
