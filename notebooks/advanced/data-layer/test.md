```
chia rpc data_layer create_data_store | jq
```
```json
{
  "id": "f946507a49e5654bdf4e68d64469e9011cd4dd490f86a86fe99f6bf9118618ec",
  "success": true,
  "txs": [
    {
      "additions": [
        {
          "amount": 1,
          "parent_coin_info": "0x612bc29d3e68350db63d8d24f37d2a67e810c49fafeb162cc4f5c4537335090e",
          "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
        },
        {
          "amount": 248999999999,
          "parent_coin_info": "0x612bc29d3e68350db63d8d24f37d2a67e810c49fafeb162cc4f5c4537335090e",
          "puzzle_hash": "0x206d641f5aae663fe2b599e1da38dfca84902e678e455dcffe65600966ff0d24"
        },
        {
          "amount": 1,
          "parent_coin_info": "0xf946507a49e5654bdf4e68d64469e9011cd4dd490f86a86fe99f6bf9118618ec",
          "puzzle_hash": "0x1108e3d0692d982a2247b8a0e8ea9230dd893dd84a5a8d0b09413db207d2b4d6"
        }
      ],
      "amount": 1,
      "confirmed": false,
      "confirmed_at_height": 0,
      "created_at_time": 1663427642,
      "fee_amount": 1000000000,
      "memos": [],
      "name": "0x83c02d90decaf4131498707b7b96d5e0c73ba94c416c97dee9ee8f9d319ce979",
      "removals": [
        {
          "amount": 250000000000,
          "parent_coin_info": "0xfe9a2901d7edb0e364e94266d0e095f700000000000000000000000000000002",
          "puzzle_hash": "0x99e07e8fbf87ddf3f72af29e3945f35f8a04c02d4e04600f3dc4964e4167045d"
        },
        {
          "amount": 1,
          "parent_coin_info": "0x612bc29d3e68350db63d8d24f37d2a67e810c49fafeb162cc4f5c4537335090e",
          "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
        }
      ],
      "sent": 10,
      "sent_to": [],
      "spend_bundle": {
        "aggregated_signature": "0xa787f397d3fd4fbbe8eb3cb87247c17140e1d87afd298e98dc81747f3842b4a2eabf7245f72a188b344a80edb7c7cde5151a2c04f27d8cd24e84e558ffb43c4b5c9b077d5599fe45f1f83191932f4ca3d9aca0d52d3164f348c043776a6cb93f",
        "coin_spends": [
          {
            "coin": {
              "amount": 250000000000,
              "parent_coin_info": "0xfe9a2901d7edb0e364e94266d0e095f700000000000000000000000000000002",
              "puzzle_hash": "0x99e07e8fbf87ddf3f72af29e3945f35f8a04c02d4e04600f3dc4964e4167045d"
            },
            "puzzle_reveal": "0xff02ffff01ff02ffff01ff02ffff03ff0bffff01ff02ffff03ffff09ff05ffff1dff0bffff1effff0bff0bffff02ff06ffff04ff02ffff04ff17ff8080808080808080ffff01ff02ff17ff2f80ffff01ff088080ff0180ffff01ff04ffff04ff04ffff04ff05ffff04ffff02ff06ffff04ff02ffff04ff17ff80808080ff80808080ffff02ff17ff2f808080ff0180ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01b0824f45f882649b634c2cbbb94292cd30e76f96448e86f297e3e4a08dffe6bc494c7450cbfb6c4650fb5c6cb161c6ae3cff018080",
            "solution": "0xff80ffff01ffff33ffa0eff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9ff0180ffff33ffa0206d641f5aae663fe2b599e1da38dfca84902e678e455dcffe65600966ff0d24ff8539f98e79ff80ffff34ff843b9aca0080ffff3cffa089d87a176b506d14796615d89765df89c3eaf2eb708ac028e7cd25b01d0c556380ffff3dffa0587b00ae06f4ea62c8def65d686cfe24493aec272c51c38cdaaf842b715331438080ff8080"
          },
          {
            "coin": {
              "amount": 1,
              "parent_coin_info": "0x612bc29d3e68350db63d8d24f37d2a67e810c49fafeb162cc4f5c4537335090e",
              "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
            },
            "puzzle_reveal": "0xff02ffff01ff04ffff04ff04ffff04ff05ffff04ff0bff80808080ffff04ffff04ff0affff04ffff02ff0effff04ff02ffff04ffff04ff05ffff04ff0bffff04ff17ff80808080ff80808080ff808080ff808080ffff04ffff01ff33ff3cff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff0effff04ff02ffff04ff09ff80808080ffff02ff0effff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080",
            "solution": "0xffa01108e3d0692d982a2247b8a0e8ea9230dd893dd84a5a8d0b09413db207d2b4d6ff01ffffa00000000000000000000000000000000000000000000000000000000000000000ffa058ebf142884c18e0cbc9d7bc0ccf46e749a4be22229f6a8ab01f864affe5fc148080"
          }
        ]
      },
      "to_puzzle_hash": "0x0202020202020202020202020202020202020202020202020202020202020202",
      "trade_id": null,
      "type": 0,
      "wallet_id": 0
    },
    {
      "additions": [
        {
          "amount": 1,
          "parent_coin_info": "0x612bc29d3e68350db63d8d24f37d2a67e810c49fafeb162cc4f5c4537335090e",
          "puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9"
        },
        {
          "amount": 248999999999,
          "parent_coin_info": "0x612bc29d3e68350db63d8d24f37d2a67e810c49fafeb162cc4f5c4537335090e",
          "puzzle_hash": "0x206d641f5aae663fe2b599e1da38dfca84902e678e455dcffe65600966ff0d24"
        }
      ],
      "amount": 1,
      "confirmed": false,
      "confirmed_at_height": 0,
      "created_at_time": 1663427642,
      "fee_amount": 1000000000,
      "memos": [],
      "name": "0xef94b2ed4ad9ca17c6026e51658d2872310a9ede08892f7b429f2809705e8e4c",
      "removals": [
        {
          "amount": 250000000000,
          "parent_coin_info": "0xfe9a2901d7edb0e364e94266d0e095f700000000000000000000000000000002",
          "puzzle_hash": "0x99e07e8fbf87ddf3f72af29e3945f35f8a04c02d4e04600f3dc4964e4167045d"
        }
      ],
      "sent": 0,
      "sent_to": [],
      "spend_bundle": null,
      "to_puzzle_hash": "0xeff07522495060c066f66f32acc2a77e3a3e737aca8baea4d1a64ea4cdc13da9",
      "trade_id": null,
      "type": 1,
      "wallet_id": 1
    }
  ]
}
```

```
❯ $store_id = 'f946507a49e5654bdf4e68d64469e9011cd4dd490f86a86fe99f6bf9118618ec'
❯ $value = opc ./the-code-book.clvm
❯ $payload = @{ id = $store_id; key = (brun '(sha256 1)' $value); value = $value } | ConvertTo-ChiaRpcJson
❯ chia rpc data_layer insert $payload
❯ chia rpc data_layer get_keys_values (@{ id = $store_id } | ConvertTo-ChiaRpcJson) | jq
{
  "keys_values": [
    {
      "atom": null,
      "hash": "0xa1594d77e0e80d09784c7755d7c3a28de4f6ba256c0b3868bc8bd22e7d6ad3a1",
      "key": "0x81fee354496d31925966a66a17d3555852dbe26f12acc8c9fd56b5d7fb5fb714",
      "value": "0xff8d54686520436f646520426f6f6bffff87417574686f7273ffff8b53696d6f6e2053696e67688080ffff83557269ffc18268747470733a2f2f7777772e616d617a6f6e2e636f6d2f436f64652d426f6f6b2d536369656e63652d536563726563792d43727970746f6772617068792d65626f6f6b2f64702f42303034494b38504c452f7265663d73725f315f313f67636c69643d436a774b43416a77344a575a4268417045697741744a554e30423772685847547a376c6c3349554d67654f66466b46394b5f724c44746455306d6551373861686d777a5a523443495f56393639426f434d6b49514176445f427745266876616469643d3631363939313232303637372668766465763d632668766c6f63696e743d393031333138342668766c6f637068793d393037333336362668766e6574773d67266876716d743d6526687672616e643d343037303039333238303739393734353137302668767461726769643d6b77642d363534343530343026687964616463723d32343636325f3133363131383032266b6579776f7264733d7468652b636f64652b626f6f6b267169643d313636333432353533352673723d382d318080"
    }
  ],
  "success": true
}
❯ opd (chia rpc data_layer get_keys_values (@{ id = $store_id } | ConvertTo-ChiaRpcJson) | ConvertFrom-Json).keys_values[0].value.SubString(2)
("The Code Book" ("Authors" ("Simon Singh")) ("Uri" "https://www.amazon.com/Code-Book-Science-Secrecy-Cryptography-ebook/dp/B004IK8PLE/ref=sr_1_1?gclid=CjwKCAjw4JWZBhApEiwAtJUN0B7rhXGTz7ll3IUMgeOfFkF9K_rLDtdU0meQ78ahmwzZR4CI_V969BoCMkIQAvD_BwE&hvadid=616991220677&hvdev=c&hvlocint=9013184&hvlocphy=9073366&hvnetw=g&hvqmt=e&hvrand=4070093280799745170&hvtargid=kwd-65445040&hydadcr=24662_13611802&keywords=the+code+book&qid=1663425535&sr=8-1"))

notebooks/advanced/data-layer on  data-layer [?]
❯ chia rpc data_layer get_root_history (@{ id = $store_id } | ConvertTo-ChiaRpcJson) | jq
{
  "root_history": [
    {
      "confirmed": true,
      "root_hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "timestamp": 1663427642
    },
    {
      "confirmed": true,
      "root_hash": "0xa1594d77e0e80d09784c7755d7c3a28de4f6ba256c0b3868bc8bd22e7d6ad3a1",
      "timestamp": 1663428140
    }
  ],
  "success": true
}
```

```
❯ chia rpc data_layer get_owned_stores | jq
{
  "store_ids": [
    "de5eefe228c2b809275270f5955ff1f312cc6901281de7cf6e0c7a2622768627",
    "f946507a49e5654bdf4e68d64469e9011cd4dd490f86a86fe99f6bf9118618ec"
  ],
  "success": true
}
```

``` PowerShell
Get-Content ./get-book-authors.clsp | % { (Format-Hex -InputObject $_ -Encoding UTF-8 | Select-Object -Expand Bytes | ForEach-Object { '{0:x2}' -f $_ }) -join ''}
286d6f6420285f20285f20617574686f727329205f29
20202020617574686f7273
29
```