# Aggregated Signature & Key

We have learned that we need `AGG_SIG_ME` condition(s) to secure our coin and spend bundle. We also learned that Chia uses BLS enabling multiple signatures to be compressed into a single signature called **aggregated signature**. This means we can put one aggregated signature into the spend bundle and save the space.

## Use Multiple Public Keys

To verify multiple signatures, the most obvios way is to add multiple `AGG_SIG_ME` conditions to verify that [the aggregated signature is the aggregate of signatures](https://chialisp.com/docs/coins_spends_and_wallets#bls-aggregated-signatures) signed by every participant we need.

```lisp
(mod (
        my_amount
        to_puzzle_hash
        pks
     )

    (include condition_codes.clib)

    (defun agg_sig_me (keys my_amount) 
        (if (l keys)
            (c 
                (list AGG_SIG_ME (f keys) (sha256 my_amount))
                (agg_sig_me (r keys) my_amount)
            )
            ()
        )
    )

    (defun merge_lists (l1 l2)
        (if (l l1)
            (c (f l1) (merge_lists (r l1) l2))
            l2
        )
    )

    (merge_lists
        (list
            (list CREATE_COIN to_puzzle_hash my_amount)
            (list ASSERT_MY_AMOUNT my_amount)
        )
        (agg_sig_me pks my_amount)
    )
)
```

When the chialisp code above is run, multiple `AGG_SIG_ME` conditions will be created. From now on, we will start using blockchain simulator instead of the **testnet**. 

_The [driver code](agg_sig_coin_pks.py) also shows how the aggregated signatures are created and if it is valid._

We can also verify the aggregated signature using `cdv inspect spendbundles` as usual.

```sh
❯ cdv inspect spendbundles ./agg_sig_coin_pks.json -db -sd
...
brun -y main.sym '(a (q 2 30 (c 2 (c (c (c 10 (c 11 (c 5 ()))) (c (c 12 (c 5 ())) ())) (c (a 22 (c 2 (c 23 (c 5 ())))) ())))) (c (q (50 . 73) 51 (a (i (l 5) (q 4 (c 8 (c 9 (c (sha256 11) ()))) (a 22 (c 2 (c 13 (c 11 ()))))) ()) 1) 2 (i (l 5) (q 4 9 (a 30 (c 2 (c 13 (c 11 ()))))) (q . 11)) 1) 1))' '(0x00e8d4a51000 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 (0x99366bea4a3c8de397218d23a1b24ad94e80b31afc9a26e1c449b7e890b1adc4576d0b70d15d4ac594a62133dec0d32e 0xa9c4bf8f10e557e2046db98ea20c8e6dd4026929d1712e7fd667c324122fedf3d672f420dc01cadda3794a4c4a868077 0x93eb9260040bff632150bad1e26fed47b904594634c1b8a822a5fe156df4a41cf5a58a2e5b17ccf97edc0685aeac0a1a))'

((CREATE_COIN 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0x00e8d4a51000) (ASSERT_MY_AMOUNT 0x00e8d4a51000) (AGG_SIG_ME 0x99366bea4a3c8de397218d23a1b24ad94e80b31afc9a26e1c449b7e890b1adc4576d0b70d15d4ac594a62133dec0d32e 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c) (AGG_SIG_ME 0xa9c4bf8f10e557e2046db98ea20c8e6dd4026929d1712e7fd667c324122fedf3d672f420dc01cadda3794a4c4a868077 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c) (AGG_SIG_ME 0x93eb9260040bff632150bad1e26fed47b904594634c1b8a822a5fe156df4a41cf5a58a2e5b17ccf97edc0685aeac0a1a 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c))

grouped conditions:

  (CREATE_COIN 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0x00e8d4a51000)

  (ASSERT_MY_AMOUNT 0x00e8d4a51000)

  (AGG_SIG_ME 0x99366bea4a3c8de397218d23a1b24ad94e80b31afc9a26e1c449b7e890b1adc4576d0b70d15d4ac594a62133dec0d32e 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c)
  (AGG_SIG_ME 0xa9c4bf8f10e557e2046db98ea20c8e6dd4026929d1712e7fd667c324122fedf3d672f420dc01cadda3794a4c4a868077 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c)
  (AGG_SIG_ME 0x93eb9260040bff632150bad1e26fed47b904594634c1b8a822a5fe156df4a41cf5a58a2e5b17ccf97edc0685aeac0a1a 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c)
...
================================================================================

aggregated signature check pass: True
pks: [<G1Element 99366bea4a3c8de397218d23a1b24ad94e80b31afc9a26e1c449b7e890b1adc4576d0b70d15d4ac594a62133dec0d32e>, <G1Element a9c4bf8f10e557e2046db98ea20c8e6dd4026929d1712e7fd667c324122fedf3d672f420dc01cadda3794a4c4a868077>, <G1Element 93eb9260040bff632150bad1e26fed47b904594634c1b8a822a5fe156df4a41cf5a58a2e5b17ccf97edc0685aeac0a1a>]
msgs: ['19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4dccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb', '19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4dccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb', '19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4dccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb']
  msg_data: ['19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c', '19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c', '19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c']
  coin_ids: ['4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4d', '4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4d', '4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4d']
  add_data: ['ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb', 'ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb', 'ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb']
signature: b51bd40ff6b3fb4994ed18f8a5c03be630af94bcb5a9a424987e9d73deae0057ec1c015a2a25690f4c957da53d3a28c60eea670121e1e0c5a3a59459bf87867af60aa6b8cd9e7ef6204ac3bc12b9ffe2074fa9f01eeaa62c4b8d4bd2ac4ab67d
None

Public Key/Message Pairs
------------------------
99366bea4a3c8de397218d23a1b24ad94e80b31afc9a26e1c449b7e890b1adc4576d0b70d15d4ac594a62133dec0d32e:
        - 19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4dccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb
a9c4bf8f10e557e2046db98ea20c8e6dd4026929d1712e7fd667c324122fedf3d672f420dc01cadda3794a4c4a868077:
        - 19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4dccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb
93eb9260040bff632150bad1e26fed47b904594634c1b8a822a5fe156df4a41cf5a58a2e5b17ccf97edc0685aeac0a1a:
        - 19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c4a9cc5566a38e3c01df5f29d822e5b7296ea826d16c3cec7abe822d47fdd1e4dccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb
```

However, we need to provide a public key for each `AGG_SIG_ME` condition. The bigger solution and more conditions will increase our CLVM cost. Our chialisp code also needs to create `AGG_SIG_ME` condition dynamically. 

```sh
❯ brun (run ./agg_sig_coin_pks.clsp -i ../include) '(0x00e8d4a51000 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 (0x99366bea4a3c8de397218d23a1b24ad94e80b31afc9a26e1c449b7e890b1adc4576d0b70d15d4ac594a62133dec0d32e 0xa9c4bf8f10e557e2046db98ea20c8e6dd4026929d1712e7fd667c324122fedf3d672f420dc01cadda3794a4c4a868077 0x93eb9260040bff632150bad1e26fed47b904594634c1b8a822a5fe156df4a41cf5a58a2e5b17ccf97edc0685aeac0a1a))' -c --time 
cost = 9727
assemble_from_ir: 0.045655
to_sexp_f: 0.000324
run_program: 0.010753
((51 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0x00e8d4a51000) (73 0x00e8d4a51000) (50 0x99366bea4a3c8de397218d23a1b24ad94e80b31afc9a26e1c449b7e890b1adc4576d0b70d15d4ac594a62133dec0d32e 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c) (50 0xa9c4bf8f10e557e2046db98ea20c8e6dd4026929d1712e7fd667c324122fedf3d672f420dc01cadda3794a4c4a868077 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c) (50 0x93eb9260040bff632150bad1e26fed47b904594634c1b8a822a5fe156df4a41cf5a58a2e5b17ccf97edc0685aeac0a1a 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c))
```

## Use Aggregated Public Key

Blockchain is an expensive resource, so we should reduce the computation cost needed as much as possible. In Chia, we should put only necessary code in Chialisp and let the driver code takes care the rest.

Besides aggregated signature, BLS also supports a distributed key generation (DKG) that allow public keys to be aggregated.

In our chialisp code below, instead of a list of public keys, we can provide an aggregated public key. Only one `AGG_SIG_ME` is now required to verify the aggregrated signature.

```lisp
(mod (
        my_amount
        to_puzzle_hash
        agg_pk
     )

    (include condition_codes.clib)

    (list
        (list CREATE_COIN to_puzzle_hash my_amount)
        (list ASSERT_MY_AMOUNT my_amount)
        (list AGG_SIG_ME agg_pk (sha256 my_amount))
    )
)
```
_Our [driver code](agg_sig_coin_agg_pk.py) is also similarto the [multiple public key one](agg_sig_coin_pks.py)_.

```sh
❯ cdv inspect spendbundles ./agg_sig_coin_agg_pk.json -db -sd 
...
brun -y main.sym '(a (q 4 (c 14 (c 11 (c 5 ()))) (c (c 10 (c 5 ())) (c (c 4 (c 23 (c (sha256 5) ()))) ()))) (c (q 50 73 . 51) 1))' '(0x00e8d4a51000 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0xa9223edd73ee9fcdf0ebc1d1df796d400e9aef4a3c3c52067ced681b101c08c5dae3abfe8f325132433d38b2c65ae855)'

((CREATE_COIN 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0x00e8d4a51000) (ASSERT_MY_AMOUNT 0x00e8d4a51000) (AGG_SIG_ME 0xa9223edd73ee9fcdf0ebc1d1df796d400e9aef4a3c3c52067ced681b101c08c5dae3abfe8f325132433d38b2c65ae855 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c))

grouped conditions:

  (CREATE_COIN 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0x00e8d4a51000)

  (ASSERT_MY_AMOUNT 0x00e8d4a51000)

  (AGG_SIG_ME 0xa9223edd73ee9fcdf0ebc1d1df796d400e9aef4a3c3c52067ced681b101c08c5dae3abfe8f325132433d38b2c65ae855 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c)

...

================================================================================

aggregated signature check pass: True
pks: [<G1Element a9223edd73ee9fcdf0ebc1d1df796d400e9aef4a3c3c52067ced681b101c08c5dae3abfe8f325132433d38b2c65ae855>]
msgs: ['19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86cfce0f70488480693515ad997642c81253dc4af75230b9f4e70ba8108f1844776ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb']
  msg_data: ['19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c']
  coin_ids: ['fce0f70488480693515ad997642c81253dc4af75230b9f4e70ba8108f1844776']
  add_data: ['ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb']
signature: b4b337bd782c7428e019bbcecb7b2b7f842a5682b4381d0fe086e3a5c3ef8b8af3d0b0ff14cfbaaaf923b8df92a48d340fb784dbbeac620ed2ed294a65a11f5e89ad1ab985e5a74e4bde441fbe088020929205acc1aa03bfc8d0780142726f59
None

Public Key/Message Pairs
------------------------
a9223edd73ee9fcdf0ebc1d1df796d400e9aef4a3c3c52067ced681b101c08c5dae3abfe8f325132433d38b2c65ae855:
        - 19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86cfce0f70488480693515ad997642c81253dc4af75230b9f4e70ba8108f1844776ccd5bb71183532bff220ba46c268991a3ff07eb358e8255a65c30a2dce0e5fbb
```

With three public keys, the aggregated public key version works like the multiple public key one, but the CLVM cost is reduced heavily from **9727** to **1962**.

> The multiple key version cost also increases when more public keys are needed while the aggregated key version cost should be independent from number of public keys!

```sh
❯ brun (run ./agg_sig_coin_agg_pk.clsp -i ../include) '(0x00e8d4a51000 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0xa9223edd73ee9fcdf0ebc1d1df796d400e9aef4a3c3c52067ced681b101c08c5dae3abfe8f325132433d38b2c65ae855)' -c --time 
cost = 1962
assemble_from_ir: 0.013310
to_sexp_f: 0.000394
run_program: 0.002062
((51 0x5abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6 0x00e8d4a51000) (73 0x00e8d4a51000) (50 0xa9223edd73ee9fcdf0ebc1d1df796d400e9aef4a3c3c52067ced681b101c08c5dae3abfe8f325132433d38b2c65ae855 0x19b6f428a262c387186c195922d543d88492ba7d83f204d5a03f2004d741b86c))
```

## Conclusions

In this post we learn how we could improve our chialisp puzzle by utilizing DKG. The driver code also shows how we utilize a blockchain simulator which make the test easier.

> [BLS has the property that the signatures of any number of (key, value) pairs can be expressed as a single aggregated signature. It isn’t possible given the aggregated signature to pull out any of the individual signatures.](https://www.chia.net/2021/05/27/Agrgregated-Sigs-Taproot-Graftroot.html)

## References
- [Aggregated Signatures, Taproot, Graftroot, and Standard Transactions](https://www.chia.net/2021/05/27/Agrgregated-Sigs-Taproot-Graftroot.html)
- [Difference between shamir secret sharing (SSS) vs Multisig vs aggregated signatures (BLS) vs distributed key generation (dkg) vs threshold signatures](https://www.cryptologie.net/article/486/difference-between-shamir-secret-sharing-sss-vs-multisig-vs-aggregated-signatures-bls-vs-distributed-key-generation-dkg-vs-threshold-signatures/)
- [BLS Deep Dive](https://skale.network/blog/bls-deep-dive)
- [Aggregatable Distributed Key Generation](https://www.benthamsgaze.org/2021/03/24/aggregatable-distributed-key-generation/)