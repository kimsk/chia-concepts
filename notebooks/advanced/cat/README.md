## References
- [CATs Primitives](https://chialisp.com/cats)
- [CATs, Offers and NFTs](https://docs.chia.net/guides/crash-course/cats-offers-nfts)
- [Single Issuance Chia Asset Token (CAT) | Chialisp](https://www.youtube.com/watch?v=yxagP_VC8BE&list=PLmnzWPUjpmaHSS_F2VPyeK35iTMlUmhSk&index=2)
- []



## Puzzles
### CAT puzzle
> Chia Asset Tokens are fungible tokens that are issued on the Chia blockchain. **The CAT puzzle ensures that the supply of a specific CAT never changes unless the rules of issuance specific to that CAT are followed.** 

> These are enforced using a separate Chialisp program called the **Token and Asset Issuance Limitations (TAIL)**.

### TAIL puzzle
> the TAIL program is run when a coin is spent to check if the issuance is valid.

All tails need 5 arguments:
`Truths`, `parent_is_cat`, `lineage_proof`, `delta`, `inner_conditions`


### Truths
```clojure
  (defun-inline my_coin_info_truth (Truths) (r (r Truths)))
  (defun-inline my_parent_cat_truth (Truths) (f (my_coin_info_truth Truths)))
```

CAT Truths is: ((Inner puzzle hash . (MOD hash . (MOD hash hash . TAIL hash))) . (my_id . (my_parent_info my_puzhash my_amount)))

#### Single-Issuance TAIL

> The single-issuance TAIL prevents melting and requires the parent to be a specific coin. This is currently the default way to issue CATs, since it ensures the supply will never increase.

- `GENESIS_ID` or a coin id of a genesis coin (a coin that create CAT coins). Once the CAT coins are created, the genesis coin is spent.
- `Truths`
- `parent_is_cat`
- `lineage_proof`
- `delta` is not zero (true) if we try to mint (create) or melt (remove) CAT coins.
- `inner_conditions`


[genesis_by_coin_id](./references/genesis_by_coin_id.clsp)
```clojure
(mod (
      GENESIS_ID
      Truths
      parent_is_cat
      lineage_proof
      delta
      inner_conditions
      _ ; solution (usually null)
    )

    (include cat_truths.clib)

    (if delta 
        (x)   ; Only allow original issuance
        (if (= (my_parent_cat_truth Truths) GENESIS_ID) ; if parent id is genesis id, issuance is allowed
          ()
          (x)
        )
    )

)
```


#### Multi-Issuance TAIL

[delegated_tail.clsp](./references/delegated_tail.clsp)

```clojure
(
      PUBKEY
      Truths
      parent_is_cat
      lineage_proof
      delta
      inner_conditions
      (
        delegated_puzzle
        delegated_solution
      )
    )
```

- Need valid signature for `PUBKEY` and `delegated_puzzle` hash.
- Allow flexible `delegated_puzzle` to be run.
```clojure
(AGG_SIG_UNSAFE PUBKEY (sha256tree1 delegated_puzzle))
(
     a 
     delegated_puzzle 
     (c Truths (c parent_is_cat (c lineage_proof (c delta (c inner_conditions delegated_solution)))))
)

```

> The multi-issuance TAIL allows any action to be taken, providing the original issuance key is used. Each spend that makes supply changes must be signed separately using this same key.

> This TAIL provides a balance between security and flexibility. It's similar to the previous TAIL, but the signature can be reused for the puzzle it's signed with, allowing the TAIL to change over time. The creator can publish the signature, allowing any owner to run the TAIL on their CAT, but any permissions granted can never be revoked.

### Inner puzzle
> Aside from the TAIL, there is also an **inner puzzle** that the CAT wraps around. The inner puzzle controls the ownership of the specific coin, and when the coin is spent, the new puzzle is wrapped in the CAT again. **Typically, you wrap the standard transaction so that you can send CATs to Chia wallet addresses.**