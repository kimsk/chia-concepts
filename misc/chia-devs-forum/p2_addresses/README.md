# [One address to redirect to several addresses.](https://developers.chia.net/t/one-address-to-redirect-to-several-addresses/572)
## Question
As the Title says, “One address to redirect to multiple addresses.”
I’m trying to find out if this functionality is possible. I didn’t see anything in the whitepaper about it but I think it would be a great opportunity that traditional banks don’t offer :grinning:

## Answer
Good question! I think we could achieve this by creating a coin that when it is spent, it will create multiple coins for multiple addresses.

The puzzle `p2_addresses.clsp` could look like this:

```clojure
(mod (PUZZLE_HASHES total_amount amount)
    (include condition_codes.clib)

    (defun pay_to (puzzle_hashes amount)
        (if (l puzzle_hashes)
        (c 
            (list CREATE_COIN (f puzzle_hashes) amount)
            (pay_to (r puzzle_hashes) amount)
        )
        ()
        )
    )

    (c
        (list ASSERT_MY_AMOUNT total_amount)
        (pay_to PUZZLE_HASHES amount)
    )
)
```

Then we can curry in the list of puzzle hashes that we want to redirect. For example, if we want to send to three addresses:

```clojure
(
   0x79a4034c96a1c841bde9fcaa719879b723f8e6fe21f4f8d33da3105590abe39e
   0x9911c986fa81f7db76f6b110cee66deb11690b67f204fe290b3396b0824f467a
   0xca2d649e52b48d7da1d29ac661c99385422b2bc4cfdaaad97fde98f57a9cf526
)
```

```sh
❯ cdv clsp curry ./p2_addresses.clsp.hex -a '(0x79a4034c96a1c841bde9fcaa719879b723f8e6fe21f4f8d33da3105590abe39e 0x9911c986fa81f7db76f6b110cee66deb11690b67f204fe290b3396b0824f467a 0xca2d649e52b48d7da1d29ac661c99385422b2bc4cfdaaad97fde98f57a9cf526)'
(a (q 2 (q 4 (c 4 (c 11 ())) (a 14 (c 2 (c 5 (c 23 ()))))) (c (q 73 51 2 (i (l 5) (q 4 (c 10 (c 9 (c 11 ()))) (a 14 (c 2 (c 13 (c 11 ()))))) ()) 1) 1)) (c (q 0x79a4034c96a1c841bde9fcaa719879b723f8e6fe21f4f8d33da3105590abe39e 0x9911c986fa81f7db76f6b110cee66deb11690b67f204fe290b3396b0824f467a 0xca2d649e52b48d7da1d29ac661c99385422b2bc4cfdaaad97fde98f57a9cf526) 1))
```

We can spend a coin with the puzzle above and it should send three coins to those three addresses:
```sh
❯ brun '(a (q 2 (q 4 (c 4 (c 11 ())) (a 14 (c 2 (c 5 (c 23 ()))))) (c (q 73 51 2 (i (l 5) (q 4 (c 10 (c 9 (c 11 ()))) (a 14 (c 2 (c 13 (c 11 ()))))) ()) 1) 1)) (c (q 0x79a4034c96a1c841bde9fcaa719879b723f8e6fe21f4f8d33da3105590abe39e 0x9911c986fa81f7db76f6b110cee66deb11690b67f204fe290b3396b0824f467a 0xca2d649e52b48d7da1d29ac661c99385422b2bc4cfdaaad97fde98f57a9cf526) 1))' '(30 10)'
((73 30) (51 0x79a4034c96a1c841bde9fcaa719879b723f8e6fe21f4f8d33da3105590abe39e 10) (51 0x9911c986fa81f7db76f6b110cee66deb11690b67f204fe290b3396b0824f467a 10) (51 0xca2d649e52b48d7da1d29ac661c99385422b2bc4cfdaaad97fde98f57a9cf526 10))
```

The solution of the coin is `(30 10)`. `30` is the amount of the `p2_addresses` coin and `10` is the amount that we want to send to each new coin.