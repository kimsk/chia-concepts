# XCH
## Prepare Sender
```sh
❯ chia wallet send -f $fp -t txch1hg828n53app237aan8kvr94hwkv70ak3eefgaqjjh4s4f6w0mydqdutqkw -a 5 -m 0.005
❯ chia wallet send -f $fp -t txch1hg828n53app237aan8kvr94hwkv70ak3eefgaqjjh4s4f6w0mydqdutqkw -i 3 -a 5 -m 0.005
```

## Sender
```sh
Fingerprint: 3436710054
Master public key (m): 814ffd60c1016cca49f7c418396127f9a1843b5f69df41f88c06a09fa565d5379feb01300f8177d9410e81050522c8f6
Farmer public key (m/12381/8444/0/0): 8580ff8c3aa41c23c87d0ea675d6ba95f41a86d07943911503c005e0aa140f8dc01e5b06b824a44738df8d6a0a5191f2
Pool public key (m/12381/8444/1/0): b58585dbfa62bd7fa6edc2f873304f8ab7bc484880272b33bb04a5e009ce6067661e8fd6e81239d3a718cd0fe21b69b0
First wallet address: txch1hg828n53app237aan8kvr94hwkv70ak3eefgaqjjh4s4f6w0mydqdutqkw

Wallet height: 1278244
Sync status: Synced
Balances, fingerprint: 3436710054

Chia Wallet:
   -Total Balance:         5.0 txch (5000000000000 mojo)
   -Pending Total Balance: 5.0 txch (5000000000000 mojo)
   -Spendable:             5.0 txch (5000000000000 mojo)
   -Type:                  STANDARD_WALLET
   -Wallet ID:             1

TCHM:
   -Total Balance:         5.0  (5000 mojo)
   -Pending Total Balance: 5.0  (5000 mojo)
   -Spendable:             5.0  (5000 mojo)
   -Type:                  CAT
   -Asset ID:              af4a9c1a4bdc6fd9b38c406be37ef4ba642036679c220767929c0e0ee6466144
   -Wallet ID:             2
```


## Receiver
```sh
Fingerprint: 713431827
Master public key (m): ad1431ee3328f8ce6806da2723ca016b3a25790c3c4164b71c1923b27009638d5cb1d76060f08fbedc935b169d463f4d
Farmer public key (m/12381/8444/0/0): a31e46e3989e14a9590c19a49517f75cc53fc1c6550ee996ae2a0afa497e1cc1a7bc65732a3a05a2dfa8ac10ca621232
Pool public key (m/12381/8444/1/0): aa70abe611468cb185491a6cfc05bc0c7e7ced25265b5510af4a250eb17eac582bb8275bb11cfa10e4313efd309aa6d8
First wallet address: txch1q5wecs3d8e5le63mcjvzkdg4rnd7wlxqj45ne9sr6rgswppzk0vquv4h0p

Wallet height: 1278268
Sync status: Synced
Balances, fingerprint: 713431827

Chia Wallet:
   -Total Balance:         0.0 txch (0 mojo)
   -Pending Total Balance: 0.0 txch (0 mojo)
   -Spendable:             0.0 txch (0 mojo)
   -Type:                  STANDARD_WALLET
   -Wallet ID:             1

TCHM:
   -Total Balance:         0.0  (0 mojo)
   -Pending Total Balance: 0.0  (0 mojo)
   -Spendable:             0.0  (0 mojo)
   -Type:                  CAT
   -Asset ID:              af4a9c1a4bdc6fd9b38c406be37ef4ba642036679c220767929c0e0ee6466144
   -Wallet ID:             2
```

# TCHM
## Send TXCH
```sh
❯ chia wallet send -f $sender -t txch1q5wecs3d8e5le63mcjvzkdg4rnd7wlxqj45ne9sr6rgswppzk0vquv4h0p -a 1 -m 0.0005
❯ chia wallet show -f $receiver
Wallet height: 1278388
Sync status: Synced
Balances, fingerprint: 713431827

Chia Wallet:
   -Total Balance:         1.0 txch (1000000000000 mojo)
   -Pending Total Balance: 1.0 txch (1000000000000 mojo)
   -Spendable:             1.0 txch (1000000000000 mojo)
   -Type:                  STANDARD_WALLET
   -Wallet ID:             1

TCHM:
   -Total Balance:         0.0  (0 mojo)
   -Pending Total Balance: 0.0  (0 mojo)
   -Spendable:             0.0  (0 mojo)
   -Type:                  CAT
   -Asset ID:              af4a9c1a4bdc6fd9b38c406be37ef4ba642036679c220767929c0e0ee6466144
   -Wallet ID:             2
```

## Get Sender Address

### Get `CoinRecrd` of Receiver
```sh
❯ $receiver_address = 'txch1q5wecs3d8e5le63mcjvzkdg4rnd7wlxqj45ne9sr6rgswppzk0vquv4h0p'
❯ cdv rpc coinrecords --by puzzlehash $(cdv decode $receiver_address)
[
    {
        "coin": {
            "amount": 1000000000000,
            "parent_coin_info": "0xe3c31212e78b73a7bc33ffc58a7b0242fbe658ee4296a55f60a7fa2039d25661",
            "puzzle_hash": "0x051d9c422d3e69fcea3bc4982b35151cdbe77cc095693c9603d0d1070422b3d8"
        },
        "coinbase": false,
        "confirmed_block_index": 1278277,
        "spent_block_index": 0,
        "timestamp": 1658327303
    }
]
```

### Get `CoinRecord` of Sender
```sh
❯ $sender_coin_id = '0xe3c31212e78b73a7bc33ffc58a7b0242fbe658ee4296a55f60a7fa2039d25661'
❯ cdv rpc coinrecords --by id $sender_coin_id -nd
{
    "e3c31212e78b73a7bc33ffc58a7b0242fbe658ee4296a55f60a7fa2039d25661": {
        "coin": {
            "amount": 5000000000000,
            "parent_coin_info": "0x08b3c127d000fec59008b7682eff0f2aa1ecd11962c7ffc930c54c797bac72d3",
            "puzzle_hash": "0xba0ea3ce91e842a8fbbd99ecc196b77599e7f6d1ce528e8252bd6154e9cfd91a"
        },
        "coinbase": false,
        "confirmed_block_index": 1278227,
        "spent_block_index": 1278277,
        "timestamp": 1658326482
    }
}
```

### Get Address of Sender

Verify if it's `txch1hg828n53app237aan8kvr94hwkv70ak3eefgaqjjh4s4f6w0mydqdutqkw`

```sh
~
❯ $parent_puzzle_hash = 'ba0ea3ce91e842a8fbbd99ecc196b77599e7f6d1ce528e8252bd6154e9cfd91a'
❯ cdv encode $parent_puzzle_hash --prefix txch
txch1hg828n53app237aan8kvr94hwkv70ak3eefgaqjjh4s4f6w0mydqdutqkw

```

## Send TCHM
```sh
❯ chia wallet show -f $sender
Wallet height: 1278430
Sync status: Synced
Balances, fingerprint: 3436710054

Chia Wallet:
   -Total Balance:         3.9995 txch (3999500000000 mojo)
   -Pending Total Balance: 3.9995 txch (3999500000000 mojo)
   -Spendable:             3.9995 txch (3999500000000 mojo)
   -Type:                  STANDARD_WALLET
   -Wallet ID:             1

TCHM:
   -Total Balance:         5.0  (5000 mojo)
   -Pending Total Balance: 5.0  (5000 mojo)
   -Spendable:             5.0  (5000 mojo)
   -Type:                  CAT
   -Asset ID:              af4a9c1a4bdc6fd9b38c406be37ef4ba642036679c220767929c0e0ee6466144
   -Wallet ID:             2

❯ chia wallet send -f $sender -t txch1q5wecs3d8e5le63mcjvzkdg4rnd7wlxqj45ne9sr6rgswppzk0vquv4h0p -i 2 -a 1 -m 0.0005
```

## Get TCHM Parent Coin
```sh
❯ chia wallet show -f $receiver
Wallet height: 1278450
Sync status: Synced
Balances, fingerprint: 713431827

Chia Wallet:
   -Total Balance:         1.0 txch (1000000000000 mojo)
   -Pending Total Balance: 1.0 txch (1000000000000 mojo)
   -Spendable:             1.0 txch (1000000000000 mojo)
   -Type:                  STANDARD_WALLET
   -Wallet ID:             1

TCHM:
   -Total Balance:         1.0  (1000 mojo)
   -Pending Total Balance: 1.0  (1000 mojo)
   -Spendable:             1.0  (1000 mojo)
   -Type:                  CAT
   -Asset ID:              af4a9c1a4bdc6fd9b38c406be37ef4ba642036679c220767929c0e0ee6466144
   -Wallet ID:             2
```

```sh
> $receiver_puzzle_hash = cdv decode txch1q5wecs3d8e5le63mcjvzkdg4rnd7wlxqj45ne9sr6rgswppzk0vquv4h0p
❯ $tchm_asset_id = 'af4a9c1a4bdc6fd9b38c406be37ef4ba642036679c220767929c0e0ee6466144'
❯ cdv clsp cat_puzzle_hash --tail $tchm_asset_id $receiver_puzzle_hash
cb0306f5ef3bdda660bcb38c7c27628b3a104a14e25baa9a23be53d4ff122306
❯ $receiver_tchm_puzzle_hash = 'cb0306f5ef3bdda660bcb38c7c27628b3a104a14e25baa9a23be53d4ff122306'

# Get THCM
❯ cdv rpc coinrecords --by puzzlehash $receiver_tchm_puzzle_hash
[
    {
        "coin": {
            "amount": 1000,
            "parent_coin_info": "0x161243d38e520eeb986d365c316dd20a8dbdc326015883deac2eafd3b2db6fee",
            "puzzle_hash": "0xcb0306f5ef3bdda660bcb38c7c27628b3a104a14e25baa9a23be53d4ff122306"
        },
        "coinbase": false,
        "confirmed_block_index": 1278443,
        "spent_block_index": 0,
        "timestamp": 1658330058
    }
]

# TCHM parent
❯ $tchm_parent_coin_info = '0x161243d38e520eeb986d365c316dd20a8dbdc326015883deac2eafd3b2db6fee'
❯ cdv rpc coinrecords --by id $tchm_parent_coin_info -nd
{
    "161243d38e520eeb986d365c316dd20a8dbdc326015883deac2eafd3b2db6fee": {
        "coin": {
            "amount": 5000,
            "parent_coin_info": "0x024c7688afdf0689ed32aa14d4dd5f84646a5c4085fc7576e8c9d60a00ece8b8",
            "puzzle_hash": "0x3fefc5e71356f1c78e037d742af3820123d532815bcd2e04a42745dcd939a0a1"
        },
        "coinbase": false,
        "confirmed_block_index": 1278240,
        "spent_block_index": 1278443,
        "timestamp": 1658326642
    }
}
```

## Get XCH address from TCHM Parent CoinSpend's Solution

```sh
❯ $tchm_parent_coin_info = '0x161243d38e520eeb986d365c316dd20a8dbdc326015883deac2eafd3b2db6fee'
❯ $tchm_parent_spent_block_idx = 1278443
❯ $payload = @{ coin_id = $tchm_parent_coin_info; height = $tchm_parent_spent_block_idx } | ConvertTo-Json

~
❯ chia rpc full_node get_puzzle_and_solution $($payload -replace '"', '\"')
{
    "coin_solution": {
        "coin": {
            "amount": 5000,
            "parent_coin_info": "0x024c7688afdf0689ed32aa14d4dd5f84646a5c4085fc7576e8c9d60a00ece8b8",
            "puzzle_hash": "0x3fefc5e71356f1c78e037d742af3820123d532815bcd2e04a42745dcd939a0a1"
        },
        "puzzle_reveal": "0xff02f...80808080",
        "solution": "0xffff80ffff01ffff33ffa0051d9c422d3e69fcea3bc4982b35151cdbe77cc095693c9603d0d1070422b3d8ff8203e8ffffa0051d9c422d3e69fcea3bc4982b35151cdbe77cc095693c9603d0d1070422b3d88080ffff33ffa0a9bcff9a8db5f62b6d1713b8517274a09d320dc4a521189836ae44501a1eadaeff820fa080ffff3cffa080d41b950a2575f13f0133bc149fcbb4863c03d668c97371a84962bd9a3695a58080ff8080ffffa087e292e32b470f355ed72db3a621904bc74fc2b988ae2cfd56af2c050361b176ffa0d744efc17b775e4a41fa3477b5a2e7cee94819cdcd17d12d39150fc1c8d49b5eff830186a080ffa0161243d38e520eeb986d365c316dd20a8dbdc326015883deac2eafd3b2db6feeffffa0024c7688afdf0689ed32aa14d4dd5f84646a5c4085fc7576e8c9d60a00ece8b8ffa03fefc5e71356f1c78e037d742af3820123d532815bcd2e04a42745dcd939a0a1ff82138880ffffa0024c7688afdf0689ed32aa14d4dd5f84646a5c4085fc7576e8c9d60a00ece8b8ffa0ba0ea3ce91e842a8fbbd99ecc196b77599e7f6d1ce528e8252bd6154e9cfd91aff82138880ff80ff8080"
    },
    "success": true
}

# decode solution
❯ opd ffff80ffff01ffff33ffa0051d9c422d3e69fcea3bc4982b35151cdbe77cc095693c9603d0d1070422b3d8ff8203e8ffffa0051d9c422d3e69fcea3bc4982b35151cdbe77cc095693c9603d0d1070422b3d88080ffff33ffa0a9bcff9a8db5f62b6d1713b8517274a09d320dc4a521189836ae44501a1eadaeff820fa080ffff3cffa080d41b950a2575f13f0133bc149fcbb4863c03d668c97371a84962bd9a3695a58080ff8080ffffa087e292e32b470f355ed72db3a621904bc74fc2b988ae2cfd56af2c050361b176ffa0d744efc17b775e4a41fa3477b5a2e7cee94819cdcd17d12d39150fc1c8d49b5eff830186a080ffa0161243d38e520eeb986d365c316dd20a8dbdc326015883deac2eafd3b2db6feeffffa0024c7688afdf0689ed32aa14d4dd5f84646a5c4085fc7576e8c9d60a00ece8b8ffa03fefc5e71356f1c78e037d742af3820123d532815bcd2e04a42745dcd939a0a1ff82138880ffffa0024c7688afdf0689ed32aa14d4dd5f84646a5c4085fc7576e8c9d60a00ece8b8ffa0ba0ea3ce91e842a8fbbd99ecc196b77599e7f6d1ce528e8252bd6154e9cfd91aff82138880ff80ff8080
(... (0x024c7688afdf0689ed32aa14d4dd5f84646a5c4085fc7576e8c9d60a00ece8b8 0xba0ea3ce91e842a8fbbd99ecc196b77599e7f6d1ce528e8252bd6154e9cfd91a 5000) () ())

❯ cdv encode ba0ea3ce91e842a8fbbd99ecc196b77599e7f6d1ce528e8252bd6154e9cfd91a --prefix txch
txch1hg828n53app237aan8kvr94hwkv70ak3eefgaqjjh4s4f6w0mydqdutqkw
```

`0xba0ea3ce91e842a8fbbd99ecc196b77599e7f6d1ce528e8252bd6154e9cfd91a` is the puzzle hash of the sender and `txch1hg828n53app237aan8kvr94hwkv70ak3eefgaqjjh4s4f6w0mydqdutqkw` is the address to which we can send anything (e.g., TCHM or NFT).
