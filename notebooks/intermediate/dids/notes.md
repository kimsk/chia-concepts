```
❯ $dids = 3214857597
❯ chia keys derive -f $dids child-key --type wallet -n 5
Wallet public key 0: ac00df28d5916c4a6881c4613a1941ec106a226d9ae78eb20ed65273cee5c83c48ed28c2a8f5b690c2e0b1012027e440
Wallet public key 1: 8cea5c2595dfae5623590d3dbd76187da637b8bea8e9b515a95ca1e62096fc411bbfbb55ce3c2c64af9680089275a321
Wallet public key 2: a9f45093d8ea15158f188b1f46a92feefce72719815f2191a19c92b54602a804ad2179659419e72c3e7bfde8df42d5f4
Wallet public key 3: 8317ee47021148eab26327227635541cddae6c02735f0ff0e65afc1a36a31206b5c9ffa2cc6ef36e6c9c8fb829e39c5a
Wallet public key 4: 879a59ec680527309a21ab6b926d87146933aa5e935ece1165b40d664fe211b7a5292143beb7f4c5ad46932f6e50a2c6

❯ chia keys derive -f $dids wallet-address -n 5
Wallet address 0: txch13emje4ep3jdj6zalwej0zzl664vdtvq59ur4pganyehzgasz98us72hux2
8e772cd7218c9b2d0bbf7664f10bfad558d5b0142f0750a3b3266e24760229f9

Wallet address 1: txch1g83u6xdgcwgknax39qd56z2wy0cu7zlaj408tj2fcy5mfk8lkmfquc8p2u
Wallet address 2: txch1mk4dw3ska5pe8jrmclxa4g4ufjsvpnqntela20qhddvmzk6ur0wqzefyf6
Wallet address 3: txch18mf3tgvwv7as8rl64kx6y5xnuwzd8lsua0xr0qddyhv8wdwm4nnsk9l8gc
Wallet address 4: txch15dyd6gtfyf488yftuafudxscqc2ych2mp85k05em2q8fkqpce26sffg88u
```

# standard coin
```
❯ cdv rpc coinrecords --by puzzlehash 0x8e772cd7218c9b2d0bbf7664f10bfad558d5b0142f0750a3b3266e24760229f9 -nd
{
    "122a12dcc939c53bb410ede0c768b5ccf78ad3afe6da3248a6faa93ad75e83d8": {
        "coin": {
            "amount": 1000000000000,
            "parent_coin_info": "0x5e8d2e86a8b4a0cbc0e935b52061fc7f8b4d27ffdf9068f38f6138bd59170966",
            "puzzle_hash": "0x8e772cd7218c9b2d0bbf7664f10bfad558d5b0142f0750a3b3266e24760229f9"
        },
        "coinbase": false,
        "confirmed_block_index": 1373191,
        "spent_block_index": 1373214,
        "timestamp": 1660271828
    }
}
```

# DID
`did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej`
```
❯ chia wallet did create -f $dids -n DID -a 3 -m 0.00005
Successfully created a DID wallet with name DID and id 2 on key 3214857597
Successfully created a DID did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej in the newly created DID wallet


❯ chia rpc wallet did_get_did '{\"wallet_id\": 2}'
{
    "coin_id": "0x992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655",
    "my_did": "did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej",
    "success": true,
    "wallet_id": 2
}

❯ chia rpc wallet did_get_current_coin_info '{\"wallet_id\": 2}'
{
    "did_amount": 3,
    "did_innerpuz": "0x0fd18d84fb127c9a182be8cdd5c09f089bb1e314aa1342e215557525797eb435",
    "did_parent": "0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752",
    "my_did": "did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej",
    "success": true,
    "wallet_id": 2
}

❯ chia rpc wallet did_get_pubkey '{\"wallet_id\": 2}'
{
    "pubkey": "8317ee47021148eab26327227635541cddae6c02735f0ff0e65afc1a36a31206b5c9ffa2cc6ef36e6c9c8fb829e39c5a",
    "success": true
}

❯ chia rpc wallet did_get_pubkey '{\"wallet_id\": 2}'
{
    "pubkey": "8317ee47021148eab26327227635541cddae6c02735f0ff0e65afc1a36a31206b5c9ffa2cc6ef36e6c9c8fb829e39c5a",
    "success": true
}
```

## puzzle_hash 0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4 
```
❯ cdv encode 81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4 --prefix txch  
txch1sx7g693kpdxg24kayxfwuexppzl259pvu3twvyxp8ew3sas68l2qzqxy3
```

## parent 0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752 (PARENT)
```
❯ cdv rpc coinrecords --by id 0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752 -nd
{
    "1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752": {
        "coin": {
            "amount": 3,
            "parent_coin_info": "0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4",
            "puzzle_hash": "0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4"
        },
        "coinbase": false,
        "confirmed_block_index": 1373214,
        "spent_block_index": 1373214,
        "timestamp": 1660272753
    }
}
```

## parent 0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 (LAUNCHER)
# launcher_id
```
❯ cdv rpc coinrecords --by id 0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 -nd
{
    "fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4": {
        "coin": {
            "amount": 3,
            "parent_coin_info": "0x122a12dcc939c53bb410ede0c768b5ccf78ad3afe6da3248a6faa93ad75e83d8",
            "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
        },
        "coinbase": false,
        "confirmed_block_index": 1373214,
        "spent_block_index": 1373214,
        "timestamp": 1660272753
    }
}
```


# DID Coin
```
❯ cdv rpc coinrecords --by id 0x992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655 -nd
{
    "992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655": {
        "coin": {
            "amount": 3,
            "parent_coin_info": "0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752",
            "puzzle_hash": "0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4"
        },
        "coinbase": false,
        "confirmed_block_index": 1373214,
        "spent_block_index": 0,
        "timestamp": 1660272753
    }
}
```

122a12dcc939c53bb410ede0c768b5ccf78ad3afe6da3248a6faa93ad75e83d8
{
    "coin": {
        "amount": 1000000000000,
        "parent_coin_info": "0x5e8d2e86a8b4a0cbc0e935b52061fc7f8b4d27ffdf9068f38f6138bd59170966",
        "puzzle_hash": "0x8e772cd7218c9b2d0bbf7664f10bfad558d5b0142f0750a3b3266e24760229f9"
    }
}

==>

fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4
{
    "coin": {
        "amount": 3,
        "parent_coin_info": "0x122a12dcc939c53bb410ede0c768b5ccf78ad3afe6da3248a6faa93ad75e83d8",
        "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
    }
}

==>

1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752
{
    "coin": {
        "amount": 3,
        "parent_coin_info": "0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4",
        "puzzle_hash": "0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4"
    }
}

==>

992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655
{
    "coin": {
        "amount": 3,
        "parent_coin_info": "0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752",
        "puzzle_hash": "0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4"
    }
}

0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4
txch1sx7g693kpdxg24kayxfwuexppzl259pvu3twvyxp8ew3sas68l2qzqxyd3

did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej

## inner_puz 0x0fd18d84fb127c9a182be8cdd5c09f089bb1e314aa1342e215557525797eb435
```
❯ cdv encode 0fd18d84fb127c9a182be8cdd5c09f089bb1e314aa1342e215557525797eb435 --prefix txch
txch1plgcmp8mzf7f5xptarxatsylpzdmrcc54gf59cs4246j27t7ks6sq8t4l6
```


## $dids_2
```
$dids_2 = 4025513928
❯ chia keys derive -f $dids_2 wallet-address -n 1
Wallet address 0: txch1w6zvmxag0pujdgz4jsnwpkz5qw2a50g852gy6zapdl0vcn9r4rtsp9eq5u
```

chia rpc wallet did_transfer_did '{\"wallet_id\": 2, \"inner_address\": \"txch1w6zvmxag0pujdgz4jsnwpkz5qw2a50g852gy6zapdl0vcn9r4rtsp9eq5u\"}'

❯ chia rpc wallet did_transfer_did '{\"wallet_id\": 2, \"inner_address\": \"txch1w6zvmxag0pujdgz4jsnwpkz5qw2a50g852gy6zapdl0vcn9r4rtsp9eq5u\"}'
{
    "success": true,
    "transaction": {
        "additions": [
            {
                "amount": 3,
                "parent_coin_info": "0x992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655",
                "puzzle_hash": "0x88a512fb5b9e4286e31d56a41d454d3d2833d876ba1753c316216839ff672fc1"
            }
        ],
        "amount": 3,
        "confirmed": false,
        "confirmed_at_height": 0,
        "created_at_time": 1660276252,
        "fee_amount": 0,
        "memos": {
            "bd502fbac6e9b8b07725b725d6198c98fc5c4bc687ba89d9cc34a23f34788808": "7684cd9ba8787926a0559426e0d8540395da3d07a2904d0ba16fdecc4ca3a8d7"
        },
        "name": "0x732600e8abbc0fa043081d3eadb37c18f0b9643a9e402033a8e02185b70e5dae",
        "removals": [
            {
                "amount": 3,
                "parent_coin_info": "0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752",
                "puzzle_hash": "0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4"
            }
        ],
        "sent": 0,
        "sent_to": [],
        "spend_bundle": {
            "aggregated_signature": "0x9365916cb3a0adeb901b838380e0afc3683e1abfd39e8a02df606843059f53ec0f060a0355f825b97b5fb8f5a6b8555a146c4d2b3a2d9f51272afee68303d84b5d64d2ae28ac134be4113c9eaf078c9d3b0be603793b8f7378e2f035150c63b3",
            "coin_spends": [
                {
                    "coin": {
                        "amount": 3,
                        "parent_coin_info": "0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752",
                        "puzzle_hash": "0x81bc8d16360b4c8556dd2192ee64c108beaa142ce456e610c13e5d18761a3fd4"
                    },
                    "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ffff03ffff18ff2fff3480ffff01ff04ffff04ff20ffff04ff2fff808080ffff04ffff02ff3effff04ff02ffff04ff05ffff04ffff02ff2affff04ff02ffff04ff27ffff04ffff02ffff03ff77ffff01ff02ff36ffff04ff02ffff04ff09ffff04ff57ffff04ffff02ff2effff04ff02ffff04ff05ff80808080ff808080808080ffff011d80ff0180ffff04ffff02ffff03ff77ffff0181b7ffff015780ff0180ff808080808080ffff04ff77ff808080808080ffff02ff3affff04ff02ffff04ff05ffff04ffff02ff0bff5f80ffff01ff8080808080808080ffff01ff088080ff0180ffff04ffff01ffffffff4947ff0233ffff0401ff0102ffffff20ff02ffff03ff05ffff01ff02ff32ffff04ff02ffff04ff0dffff04ffff0bff3cffff0bff34ff2480ffff0bff3cffff0bff3cffff0bff34ff2c80ff0980ffff0bff3cff0bffff0bff34ff8080808080ff8080808080ffff010b80ff0180ffff02ffff03ffff22ffff09ffff0dff0580ff2280ffff09ffff0dff0b80ff2280ffff15ff17ffff0181ff8080ffff01ff0bff05ff0bff1780ffff01ff088080ff0180ff02ffff03ff0bffff01ff02ffff03ffff02ff26ffff04ff02ffff04ff13ff80808080ffff01ff02ffff03ffff20ff1780ffff01ff02ffff03ffff09ff81b3ffff01818f80ffff01ff02ff3affff04ff02ffff04ff05ffff04ff1bffff04ff34ff808080808080ffff01ff04ffff04ff23ffff04ffff02ff36ffff04ff02ffff04ff09ffff04ff53ffff04ffff02ff2effff04ff02ffff04ff05ff80808080ff808080808080ff738080ffff02ff3affff04ff02ffff04ff05ffff04ff1bffff04ff34ff8080808080808080ff0180ffff01ff088080ff0180ffff01ff04ff13ffff02ff3affff04ff02ffff04ff05ffff04ff1bffff04ff17ff8080808080808080ff0180ffff01ff02ffff03ff17ff80ffff01ff088080ff018080ff0180ffffff02ffff03ffff09ff09ff3880ffff01ff02ffff03ffff18ff2dffff010180ffff01ff0101ff8080ff0180ff8080ff0180ff0bff3cffff0bff34ff2880ffff0bff3cffff0bff3cffff0bff34ff2c80ff0580ffff0bff3cffff02ff32ffff04ff02ffff04ff07ffff04ffff0bff34ff3480ff8080808080ffff0bff34ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff2effff04ff02ffff04ff09ff80808080ffff02ff2effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff02ffff03ffff21ff17ffff09ff0bff158080ffff01ff04ff30ffff04ff0bff808080ffff01ff088080ff0180ff018080ffff04ffff01ffa07faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9fffa0fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4a0eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9ffff04ffff01ff02ffff01ff02ffff01ff02ffff03ff81bfffff01ff02ff05ff82017f80ffff01ff02ffff03ffff22ffff09ffff02ff7effff04ff02ffff04ff8217ffff80808080ff0b80ffff15ff17ff808080ffff01ff04ffff04ff28ffff04ff82017fff808080ffff04ffff04ff34ffff04ff8202ffffff04ff82017fffff04ffff04ff8202ffff8080ff8080808080ffff04ffff04ff38ffff04ff822fffff808080ffff02ff26ffff04ff02ffff04ff2fffff04ff17ffff04ff8217ffffff04ff822fffffff04ff8202ffffff04ff8205ffffff04ff820bffffff01ff8080808080808080808080808080ffff01ff088080ff018080ff0180ffff04ffff01ffffffff313dff4946ffff0233ff3c04ffffff0101ff02ff02ffff03ff05ffff01ff02ff3affff04ff02ffff04ff0dffff04ffff0bff2affff0bff22ff3c80ffff0bff2affff0bff2affff0bff22ff3280ff0980ffff0bff2aff0bffff0bff22ff8080808080ff8080808080ffff010b80ff0180ffffff02ffff03ff17ffff01ff02ffff03ff82013fffff01ff04ffff04ff30ffff04ffff0bffff0bffff02ff36ffff04ff02ffff04ff05ffff04ff27ffff04ff82023fffff04ff82053fffff04ff820b3fff8080808080808080ffff02ff7effff04ff02ffff04ffff02ff2effff04ff02ffff04ff2fffff04ff5fffff04ff82017fff808080808080ff8080808080ff2f80ff808080ffff02ff26ffff04ff02ffff04ff05ffff04ff0bffff04ff37ffff04ff2fffff04ff5fffff04ff8201bfffff04ff82017fffff04ffff10ff8202ffffff010180ff808080808080808080808080ffff01ff02ff26ffff04ff02ffff04ff05ffff04ff37ffff04ff2fffff04ff5fffff04ff8201bfffff04ff82017fffff04ff8202ffff8080808080808080808080ff0180ffff01ff02ffff03ffff15ff8202ffffff11ff0bffff01018080ffff01ff04ffff04ff20ffff04ff82017fffff04ff5fff80808080ff8080ffff01ff088080ff018080ff0180ff0bff17ffff02ff5effff04ff02ffff04ff09ffff04ff2fffff04ffff02ff7effff04ff02ffff04ffff04ff09ffff04ff0bff1d8080ff80808080ff808080808080ff5f80ffff04ffff0101ffff04ffff04ff2cffff04ff05ff808080ffff04ffff04ff20ffff04ff17ffff04ff0bff80808080ff80808080ffff0bff2affff0bff22ff2480ffff0bff2affff0bff2affff0bff22ff3280ff0580ffff0bff2affff02ff3affff04ff02ffff04ff07ffff04ffff0bff22ff2280ff8080808080ffff0bff22ff8080808080ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff7effff04ff02ffff04ff09ff80808080ffff02ff7effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01ff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b08c2bb9cabf5a0dc0beddc4e95b8847faaccc4ba147c3b6c04f78e339526f152798fb876204a7ea3da4e8e3aef847d405ff018080ffff04ffff01a04bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459affff04ffff0180ffff04ffff01ffa07faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9fffa0fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4a0eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9ffff04ffff0180ff01808080808080ff01808080",
                    "solution": "0xffffa0fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4ffa00fd18d84fb127c9a182be8cdd5c09f089bb1e314aa1342e215557525797eb435ff0380ff03ffff02ffff80ffff01ffff33ffa08645d16295b80febc209afaaf3dce0aef1d81ff63e57f2f5126b18998f8ed25bff03ffffa07684cd9ba8787926a0559426e0d8540395da3d07a2904d0ba16fdecc4ca3a8d78080ffff3cffa0992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f6558080ff8080ff80ff80ff80ff808080"
                }
            ]
        },
        "to_address": "txch1w6zvmxag0pujdgz4jsnwpkz5qw2a50g852gy6zapdl0vcn9r4rtsp9eq5u",
        "to_puzzle_hash": "0x7684cd9ba8787926a0559426e0d8540395da3d07a2904d0ba16fdecc4ca3a8d7",
        "trade_id": null,
        "type": 1,
        "wallet_id": 2
    },
    "transaction_id": "0x732600e8abbc0fa043081d3eadb37c18f0b9643a9e402033a8e02185b70e5dae"
}


❯ chia wallet show -f $dids_2
Wallet height: 1373343
Sync status: Synced
Balances, fingerprint: 4025513928

Chia Wallet:
   -Total Balance:         0.0 txch (0 mojo)
   -Pending Total Balance: 0.0 txch (0 mojo)
   -Spendable:             0.0 txch (0 mojo)
   -Type:                  STANDARD_WALLET
   -Wallet ID:             1

DID did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej:
   -Total Balance:         3.0
   -Pending Total Balance: 3.0
   -Spendable:             3.0
   -Type:                  DECENTRALIZED_ID
   -DID ID:                did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej
   -Wallet ID:             2

   ❯ chia rpc wallet did_get_did '{\"wallet_id\": 2}'
{
    "coin_id": "0xbd502fbac6e9b8b07725b725d6198c98fc5c4bc687ba89d9cc34a23f34788808",
    "my_did": "did:chia:1lme5spv6h4egqxm2w6383wej3rqsp398f3tjclff2w2pshwqm8zq4xkaej",
    "success": true,
    "wallet_id": 2
}

chia-concepts on  dids [!?]
❯ cdv rpc coinrecords --by id 0xbd502fbac6e9b8b07725b725d6198c98fc5c4bc687ba89d9cc34a23f34788808 -nd
{
    "bd502fbac6e9b8b07725b725d6198c98fc5c4bc687ba89d9cc34a23f34788808": {
        "coin": {
            "amount": 3,
            "parent_coin_info": "0x992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655",
            "puzzle_hash": "0x88a512fb5b9e4286e31d56a41d454d3d2833d876ba1753c316216839ff672fc1"
        },
        "coinbase": false,
        "confirmed_block_index": 1373343,
        "spent_block_index": 0,
        "timestamp": 1660276336
    }
}


opd 'ff02ffff01ff02ffff01ff02ffff03ffff18ff2fff3480ffff01ff04ffff04ff20ffff04ff2fff808080ffff04ffff02ff3effff04ff02ffff04ff05ffff04ffff02ff2affff04ff02ffff04ff27ffff04ffff02ffff03ff77ffff01ff02ff36ffff04ff02ffff04ff09ffff04ff57ffff04ffff02ff2effff04ff02ffff04ff05ff80808080ff808080808080ffff011d80ff0180ffff04ffff02ffff03ff77ffff0181b7ffff015780ff0180ff808080808080ffff04ff77ff808080808080ffff02ff3affff04ff02ffff04ff05ffff04ffff02ff0bff5f80ffff01ff8080808080808080ffff01ff088080ff0180ffff04ffff01ffffffff4947ff0233ffff0401ff0102ffffff20ff02ffff03ff05ffff01ff02ff32ffff04ff02ffff04ff0dffff04ffff0bff3cffff0bff34ff2480ffff0bff3cffff0bff3cffff0bff34ff2c80ff0980ffff0bff3cff0bffff0bff34ff8080808080ff8080808080ffff010b80ff0180ffff02ffff03ffff22ffff09ffff0dff0580ff2280ffff09ffff0dff0b80ff2280ffff15ff17ffff0181ff8080ffff01ff0bff05ff0bff1780ffff01ff088080ff0180ff02ffff03ff0bffff01ff02ffff03ffff02ff26ffff04ff02ffff04ff13ff80808080ffff01ff02ffff03ffff20ff1780ffff01ff02ffff03ffff09ff81b3ffff01818f80ffff01ff02ff3affff04ff02ffff04ff05ffff04ff1bffff04ff34ff808080808080ffff01ff04ffff04ff23ffff04ffff02ff36ffff04ff02ffff04ff09ffff04ff53ffff04ffff02ff2effff04ff02ffff04ff05ff80808080ff808080808080ff738080ffff02ff3affff04ff02ffff04ff05ffff04ff1bffff04ff34ff8080808080808080ff0180ffff01ff088080ff0180ffff01ff04ff13ffff02ff3affff04ff02ffff04ff05ffff04ff1bffff04ff17ff8080808080808080ff0180ffff01ff02ffff03ff17ff80ffff01ff088080ff018080ff0180ffffff02ffff03ffff09ff09ff3880ffff01ff02ffff03ffff18ff2dffff010180ffff01ff0101ff8080ff0180ff8080ff0180ff0bff3cffff0bff34ff2880ffff0bff3cffff0bff3cffff0bff34ff2c80ff0580ffff0bff3cffff02ff32ffff04ff02ffff04ff07ffff04ffff0bff34ff3480ff8080808080ffff0bff34ff8080808080ffff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff2effff04ff02ffff04ff09ff80808080ffff02ff2effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff02ffff03ffff21ff17ffff09ff0bff158080ffff01ff04ff30ffff04ff0bff808080ffff01ff088080ff0180ff018080ffff04ffff01ffa07faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9fffa0fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4a0eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9ffff04ffff01ff02ffff01ff02ffff01ff02ffff03ff81bfffff01ff02ff05ff82017f80ffff01ff02ffff03ffff22ffff09ffff02ff7effff04ff02ffff04ff8217ffff80808080ff0b80ffff15ff17ff808080ffff01ff04ffff04ff28ffff04ff82017fff808080ffff04ffff04ff34ffff04ff8202ffffff04ff82017fffff04ffff04ff8202ffff8080ff8080808080ffff04ffff04ff38ffff04ff822fffff808080ffff02ff26ffff04ff02ffff04ff2fffff04ff17ffff04ff8217ffffff04ff822fffffff04ff8202ffffff04ff8205ffffff04ff820bffffff01ff8080808080808080808080808080ffff01ff088080ff018080ff0180ffff04ffff01ffffffff313dff4946ffff0233ff3c04ffffff0101ff02ff02ffff03ff05ffff01ff02ff3affff04ff02ffff04ff0dffff04ffff0bff2affff0bff22ff3c80ffff0bff2affff0bff2affff0bff22ff3280ff0980ffff0bff2aff0bffff0bff22ff8080808080ff8080808080ffff010b80ff0180ffffff02ffff03ff17ffff01ff02ffff03ff82013fffff01ff04ffff04ff30ffff04ffff0bffff0bffff02ff36ffff04ff02ffff04ff05ffff04ff27ffff04ff82023fffff04ff82053fffff04ff820b3fff8080808080808080ffff02ff7effff04ff02ffff04ffff02ff2effff04ff02ffff04ff2fffff04ff5fffff04ff82017fff808080808080ff8080808080ff2f80ff808080ffff02ff26ffff04ff02ffff04ff05ffff04ff0bffff04ff37ffff04ff2fffff04ff5fffff04ff8201bfffff04ff82017fffff04ffff10ff8202ffffff010180ff808080808080808080808080ffff01ff02ff26ffff04ff02ffff04ff05ffff04ff37ffff04ff2fffff04ff5fffff04ff8201bfffff04ff82017fffff04ff8202ffff8080808080808080808080ff0180ffff01ff02ffff03ffff15ff8202ffffff11ff0bffff01018080ffff01ff04ffff04ff20ffff04ff82017fffff04ff5fff80808080ff8080ffff01ff088080ff018080ff0180ff0bff17ffff02ff5effff04ff02ffff04ff09ffff04ff2fffff04ffff02ff7effff04ff02ffff04ffff04ff09ffff04ff0bff1d8080ff80808080ff808080808080ff5f80ffff04ffff0101ffff04ffff04ff2cffff04ff05ff808080ffff04ffff04ff20ffff04ff17ffff04ff0bff80808080ff80808080ffff0bff2affff0bff22ff2480ffff0bff2affff0bff2affff0bff22ff3280ff0580ffff0bff2affff02ff3affff04ff02ffff04ff07ffff04ffff0bff22ff2280ff8080808080ffff0bff22ff8080808080ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff7effff04ff02ffff04ff09ff80808080ffff02ff7effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01ff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b08c2bb9cabf5a0dc0beddc4e95b8847faaccc4ba147c3b6c04f78e339526f152798fb876204a7ea3da4e8e3aef847d405ff018080ffff04ffff01a04bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459affff04ffff0180ffff04ffff01ffa07faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9fffa0fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4a0eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9ffff04ffff0180ff01808080808080ff01808080'

(a (q 2 (q 2 (i (logand 47 52) (q 4 (c 32 (c 47 ())) (c (a 62 (c 2 (c 5 (c (a 42 (c 2 (c 39 (c (a (i 119 (q 2 54 (c 2 (c 9 (c 87 (c (a 46 (c 2 (c 5 ()))) ()))))) (q . 29)) 1) (c (a (i 119 (q . -73) (q . 87)) 1) ()))))) (c 119 ()))))) (a 58 (c 2 (c 5 (c (a 11 95) (q ()))))))) (q 8)) 1) (c (q (((73 . 71) 2 . 51) (c . 1) 1 . 2) ((not 2 (i 5 (q 2 50 (c 2 (c 13 (c (sha256 60 (sha256 52 36) (sha256 60 (sha256 60 (sha256 52 44) 9) (sha256 60 11 (sha256 52 ())))) ())))) (q . 11)) 1) (a (i (all (= (strlen 5) 34) (= (strlen 11) 34) (> 23 (q . -1))) (q 11 5 11 23) (q 8)) 1) 2 (i 11 (q 2 (i (a 38 (c 2 (c 19 ()))) (q 2 (i (not 23) (q 2 (i (= -77 (q . -113)) (q 2 58 (c 2 (c 5 (c 27 (c 52 ()))))) (q 4 (c 35 (c (a 54 (c 2 (c 9 (c 83 (c (a 46 (c 2 (c 5 ()))) ()))))) 115)) (a 58 (c 2 (c 5 (c 27 (c 52 ()))))))) 1) (q 8)) 1) (q 4 19 (a 58 (c 2 (c 5 (c 27 (c 23 ()))))))) 1) (q 2 (i 23 () (q 8)) 1)) 1) ((a (i (= 9 56) (q 2 (i (logand 45 (q . 1)) (q 1 . 1) ()) 1) ()) 1) 11 60 (sha256 52 40) (sha256 60 (sha256 60 (sha256 52 44) 5) (sha256 60 (a 50 (c 2 (c 7 (c (sha256 52 52) ())))) (sha256 52 ())))) (a (i (l 5) (q 11 (q . 2) (a 46 (c 2 (c 9 ()))) (a 46 (c 2 (c 13 ())))) (q 11 (q . 1) 5)) 1) 2 (i (any 23 (= 11 21)) (q 4 48 (c 11 ())) (q 8)) 1) 1)) (c (q 0x7faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9f 0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 . 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9) (c (q 2 (q 2 (q 2 (i -65 (q 2 5 383) (q 2 (i (all (= (a 126 (c 2 (c 6143 ()))) 11) (> 23 ())) (q 4 (c 40 (c 383 ())) (c (c 52 (c 767 (c 383 (c (c 767 ()) ())))) (c (c 56 (c 12287 ())) (a 38 (c 2 (c 47 (c 23 (c 6143 (c 12287 (c 767 (c 1535 (c 3071 (q ()))))))))))))) (q 8)) 1)) 1) (c (q (((49 . 61) 73 . 70) (a . 51) 60 . 4) ((q . 1) 2 2 (i 5 (q 2 58 (c 2 (c 13 (c (sha256 42 (sha256 34 60) (sha256 42 (sha256 42 (sha256 34 50) 9) (sha256 42 11 (sha256 34 ())))) ())))) (q . 11)) 1) ((a (i 23 (q 2 (i 319 (q 4 (c 48 (c (sha256 (sha256 (a 54 (c 2 (c 5 (c 39 (c 575 (c 1343 (c 2879 ()))))))) (a 126 (c 2 (c (a 46 (c 2 (c 47 (c 95 (c 383 ()))))) ())))) 47) ())) (a 38 (c 2 (c 5 (c 11 (c 55 (c 47 (c 95 (c 447 (c 383 (c (+ 767 (q . 1)) ()))))))))))) (q 2 38 (c 2 (c 5 (c 55 (c 47 (c 95 (c 447 (c 383 (c 767 ())))))))))) 1) (q 2 (i (> 767 (- 11 (q . 1))) (q 4 (c 32 (c 383 (c 95 ()))) ()) (q 8)) 1)) 1) 11 23 (a 94 (c 2 (c 9 (c 47 (c (a 126 (c 2 (c (c 9 (c 11 29)) ()))) ()))))) 95) (c (q . 1) (c (c 44 (c 5 ())) (c (c 32 (c 23 (c 11 ()))) ()))) (sha256 42 (sha256 34 36) (sha256 42 (sha256 42 (sha256 34 50) 5) (sha256 42 (a 58 (c 2 (c 7 (c (sha256 34 34) ())))) (sha256 34 ())))) 2 (i (l 5) (q 11 (q . 2) (a 126 (c 2 (c 9 ()))) (a 126 (c 2 (c 13 ())))) (q 11 (q . 1) 5)) 1) 1)) (c (q 2 (q 2 (q 2 (i 11 (q 2 (i (= 5 (point_add 11 (pubkey_for_exp (sha256 11 (a 6 (c 2 (c 23 ()))))))) (q 2 23 47) (q 8)) 1) (q 4 (c 4 (c 5 (c (a 6 (c 2 (c 23 ()))) ()))) (a 23 47))) 1) (c (q 50 2 (i (l 5) (q 11 (q . 2) (a 6 (c 2 (c 9 ()))) (a 6 (c 2 (c 13 ())))) (q 11 (q . 1) 5)) 1) 1)) (c (q . 0x8c2bb9cabf5a0dc0beddc4e95b8847faaccc4ba147c3b6c04f78e339526f152798fb876204a7ea3da4e8e3aef847d405) 1)) (c (q . 0x4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a) (c (q) (c (q 0x7faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9f 0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 . 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9) (c (q) 1)))))) 1)))

opd 'ffffa0fef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4ffa00fd18d84fb127c9a182be8cdd5c09f089bb1e314aa1342e215557525797eb435ff0380ff03ffff02ffff80ffff01ffff33ffa08645d16295b80febc209afaaf3dce0aef1d81ff63e57f2f5126b18998f8ed25bff03ffffa07684cd9ba8787926a0559426e0d8540395da3d07a2904d0ba16fdecc4ca3a8d78080ffff3cffa0992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f6558080ff8080ff80ff80ff80ff808080'

((0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 0x0fd18d84fb127c9a182be8cdd5c09f089bb1e314aa1342e215557525797eb435 3) 3 (a (() (q (51 0x8645d16295b80febc209afaaf3dce0aef1d81ff63e57f2f5126b18998f8ed25b 3 (0x7684cd9ba8787926a0559426e0d8540395da3d07a2904d0ba16fdecc4ca3a8d7)) (60 0x992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655)) ()) () () () ()))

brun '(a (q 2 (q 2 (i (logand 47 52) (q 4 (c 32 (c 47 ())) (c (a 62 (c 2 (c 5 (c (a 42 (c 2 (c 39 (c (a (i 119 (q 2 54 (c 2 (c 9 (c 87 (c (a 46 (c 2 (c 5 ()))) ()))))) (q . 29)) 1) (c (a (i 119 (q . -73) (q . 87)) 1) ()))))) (c 119 ()))))) (a 58 (c 2 (c 5 (c (a 11 95) (q ()))))))) (q 8)) 1) (c (q (((73 . 71) 2 . 51) (c . 1) 1 . 2) ((not 2 (i 5 (q 2 50 (c 2 (c 13 (c (sha256 60 (sha256 52 36) (sha256 60 (sha256 60 (sha256 52 44) 9) (sha256 60 11 (sha256 52 ())))) ())))) (q . 11)) 1) (a (i (all (= (strlen 5) 34) (= (strlen 11) 34) (> 23 (q . -1))) (q 11 5 11 23) (q 8)) 1) 2 (i 11 (q 2 (i (a 38 (c 2 (c 19 ()))) (q 2 (i (not 23) (q 2 (i (= -77 (q . -113)) (q 2 58 (c 2 (c 5 (c 27 (c 52 ()))))) (q 4 (c 35 (c (a 54 (c 2 (c 9 (c 83 (c (a 46 (c 2 (c 5 ()))) ()))))) 115)) (a 58 (c 2 (c 5 (c 27 (c 52 ()))))))) 1) (q 8)) 1) (q 4 19 (a 58 (c 2 (c 5 (c 27 (c 23 ()))))))) 1) (q 2 (i 23 () (q 8)) 1)) 1) ((a (i (= 9 56) (q 2 (i (logand 45 (q . 1)) (q 1 . 1) ()) 1) ()) 1) 11 60 (sha256 52 40) (sha256 60 (sha256 60 (sha256 52 44) 5) (sha256 60 (a 50 (c 2 (c 7 (c (sha256 52 52) ())))) (sha256 52 ())))) (a (i (l 5) (q 11 (q . 2) (a 46 (c 2 (c 9 ()))) (a 46 (c 2 (c 13 ())))) (q 11 (q . 1) 5)) 1) 2 (i (any 23 (= 11 21)) (q 4 48 (c 11 ())) (q 8)) 1) 1)) (c (q 0x7faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9f 0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 . 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9) (c (q 2 (q 2 (q 2 (i -65 (q 2 5 383) (q 2 (i (all (= (a 126 (c 2 (c 6143 ()))) 11) (> 23 ())) (q 4 (c 40 (c 383 ())) (c (c 52 (c 767 (c 383 (c (c 767 ()) ())))) (c (c 56 (c 12287 ())) (a 38 (c 2 (c 47 (c 23 (c 6143 (c 12287 (c 767 (c 1535 (c 3071 (q ()))))))))))))) (q 8)) 1)) 1) (c (q (((49 . 61) 73 . 70) (a . 51) 60 . 4) ((q . 1) 2 2 (i 5 (q 2 58 (c 2 (c 13 (c (sha256 42 (sha256 34 60) (sha256 42 (sha256 42 (sha256 34 50) 9) (sha256 42 11 (sha256 34 ())))) ())))) (q . 11)) 1) ((a (i 23 (q 2 (i 319 (q 4 (c 48 (c (sha256 (sha256 (a 54 (c 2 (c 5 (c 39 (c 575 (c 1343 (c 2879 ()))))))) (a 126 (c 2 (c (a 46 (c 2 (c 47 (c 95 (c 383 ()))))) ())))) 47) ())) (a 38 (c 2 (c 5 (c 11 (c 55 (c 47 (c 95 (c 447 (c 383 (c (+ 767 (q . 1)) ()))))))))))) (q 2 38 (c 2 (c 5 (c 55 (c 47 (c 95 (c 447 (c 383 (c 767 ())))))))))) 1) (q 2 (i (> 767 (- 11 (q . 1))) (q 4 (c 32 (c 383 (c 95 ()))) ()) (q 8)) 1)) 1) 11 23 (a 94 (c 2 (c 9 (c 47 (c (a 126 (c 2 (c (c 9 (c 11 29)) ()))) ()))))) 95) (c (q . 1) (c (c 44 (c 5 ())) (c (c 32 (c 23 (c 11 ()))) ()))) (sha256 42 (sha256 34 36) (sha256 42 (sha256 42 (sha256 34 50) 5) (sha256 42 (a 58 (c 2 (c 7 (c (sha256 34 34) ())))) (sha256 34 ())))) 2 (i (l 5) (q 11 (q . 2) (a 126 (c 2 (c 9 ()))) (a 126 (c 2 (c 13 ())))) (q 11 (q . 1) 5)) 1) 1)) (c (q 2 (q 2 (q 2 (i 11 (q 2 (i (= 5 (point_add 11 (pubkey_for_exp (sha256 11 (a 6 (c 2 (c 23 ()))))))) (q 2 23 47) (q 8)) 1) (q 4 (c 4 (c 5 (c (a 6 (c 2 (c 23 ()))) ()))) (a 23 47))) 1) (c (q 50 2 (i (l 5) (q 11 (q . 2) (a 6 (c 2 (c 9 ()))) (a 6 (c 2 (c 13 ())))) (q 11 (q . 1) 5)) 1) 1)) (c (q . 0x8c2bb9cabf5a0dc0beddc4e95b8847faaccc4ba147c3b6c04f78e339526f152798fb876204a7ea3da4e8e3aef847d405) 1)) (c (q . 0x4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a) (c (q) (c (q 0x7faa3253bfddd1e0decb0906b2dc6247bbc4cf608f58345d173adb63e8b47c9f 0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 . 0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9) (c (q) 1)))))) 1)))' '((0xfef348059abd72801b6a76a278bb3288c100c4a74c572c7d295394185dc0d9c4 0x0fd18d84fb127c9a182be8cdd5c09f089bb1e314aa1342e215557525797eb435 3) 3 (a (() (q (51 0x8645d16295b80febc209afaaf3dce0aef1d81ff63e57f2f5126b18998f8ed25b 3 (0x7684cd9ba8787926a0559426e0d8540395da3d07a2904d0ba16fdecc4ca3a8d7)) (60 0x992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655)) ()) () () () ()))'

((73 3) (71 0x1c8aa1add7a6d1adc379e464dd99943d06608de1883e188e75d7ee6cf8730752) (50 0x8c2bb9cabf5a0dc0beddc4e95b8847faaccc4ba147c3b6c04f78e339526f152798fb876204a7ea3da4e8e3aef847d405 0xdd45cf7b3b0b45d57b7cc7a1f2281791cfdb1ff74cfaca349b046d73fabaa278) (51 0x88a512fb5b9e4286e31d56a41d454d3d2833d876ba1753c316216839ff672fc1 3 (0x7684cd9ba8787926a0559426e0d8540395da3d07a2904d0ba16fdecc4ca3a8d7)) (60 0x992244f6fc769bda45cb44de99ab4a18c3350d4757148512949e1a605aa9f655))


(50 0x8c2bb9cabf5a0dc0beddc4e95b8847faaccc4ba147c3b6c04f78e339526f152798fb876204a7ea3da4e8e3aef847d405 0xdd45cf7b3b0b45d57b7cc7a1f2281791cfdb1ff74cfaca349b046d73fabaa278) 