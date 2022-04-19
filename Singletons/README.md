# Singleton

> A singleton is an identity which is embodied by exactly one coin at any given time, and where it’s possible for coins to validate that they’re interacting with the current representative of that identity. It’s similar to, but simpler than, coloured coins. An NFT is barely more than a raw singleton. Singletons are also the foundation of rate limited wallets, distributed identities, pool protocol, and price oracles. -- [A Vision for DeFi in Chia](https://www.chia.net/2021/07/13/a-vision-for-defi-in-chia.en.html)

> Singleton - A singleton is a coin that is verifiably unique. Similar to (but more powerful than) NFTs, a singleton cannot be copied, duplicated, or recreated if it is destroyed. It is a common outer puzzle for things like DIDs, NFTs, or the pooling protocol. -- [The Great Chia Glossary | Singleton](https://chialisp.com/docs/glossary)

## What
> A singleton is a special kind of puzzle that asserts **uniqueness**, preventing other coins from being mistaken for it. It can change state over time, each time creating a new puzzle based on the previous. It wraps an **inner puzzle** which can have whatever behavior you desire. These traits combined allow for smart contracts and things like NFTs to be created. -- [What is a singleton?](https://developers.chia.net/t/what-is-a-singleton/87)


Fundamentally, a singleton puzzle is the followings:
- An outer puzzle
- A puzzle with unique id

## Why
> Coins on the network are state, the puzzle is the data contained within them. You can spend them to change their state however you like, by creating new coins. This is what singletons excel at. -- [Can you store state on the network?](https://developers.chia.net/t/can-you-store-state-on-the-network/84)

### Coin Id
Each coin has a unique [coin_id](../COIN_ID.md) which derived from `parent_coin_id`, `puzzle_hash`, and its `amount` (in mojos). 

Once you spend the coin with the existing state, you could get a new unspent coin with the new state. However, this means that you have to keep track of a valid `coin_id`

### Launcher Id
In the account model (e.g, Ethereum), you have a unique contract address that you can access and update data. In the coin set model, however, coins are state, so we need to be able to extract state that we are interested from those coins somehow. To update those states, we will need to spend them and create new coins. **A singleton coin provides a unique id called launcher id that can be used as permanent unique address.** The singleton coin is spent and the new singleton coin is created, but the `launcher id` (a unique id) is always the same.

## Use Cases

### Plot NFT for Pooling
The most well-known singleton example is the [plot nft](https://github.com/Chia-Network/chia-blockchain/wiki/Pooling-FAQ#what-is-a-plot-nft), which keeps the pool that the farmer belongs to. Farmer can always switch the pool by spending the singleton plot nfg and provide the new pool information. 

> The original pool design was having pool keys in plot files, but that means if farmers want to switch pool, they'd have to re-plot!! [Pools in Chia](https://www.chia.net/2020/11/10/pools-in-chia.html)

### Others

Anything that needs to be unique on the blockchain can also be represented by a singleton.

- NFT (Non-Fungible Token) 
- DIDs (Decentralized Identifiers) : A parent singleton can be treated as DID.

## How it works?

To ensure that the coin is unique, when a singleton coin is spent, it creates another singleton coin with the same launcher id. This, however, doesn't prevent a singleton coin to create non-singleton coins.

### Rules of Singleton
- A singleton must have an odd mojo value.
- Only one output (i.e., a singleton) coin can have an odd mojo value.
- All singletons should have the same format.

## Bootstrapping

So we have set up the rules for our singleton puzzle. However, how we can create one and only-one singleton coin?

> We need to ensure that only one singleton is created with the same ID. This is surprisingly difficult. The crux of the issue is that we have no control over the coin that creates the singleton. 

> This is technically detectable by crawling up the chain and checking the first non-singleton coin to see if it had multiple singleton children, but this is inefficient and we would like all of our logic to be contained to the puzzles.

> Instead, what we can use is a launcher which is a specific puzzle that does exactly one thing: create a single singleton. We then need to curry this launcher puzzle hash into our singleton and have the first singleton assert that it, in fact, came from a parent whose puzzle hash was the launcher puzzle hash. Then, when people look at our singleton, they can see that the launcher puzzle hash is the hash of what they know to be a puzzle that creates only one singleton. They don't need to go back to the original parent and verify because the singleton puzzle takes care of that right from the start!
[The Launcher](https://chialisp.com/docs/puzzles/singletons#the-launcher)

- A first singleton coin must be created from the coin called **the Launcher** by passing in our `singleton_puzzle_hash` (as a solution).
- To make sure that the `singleton_puzzle_hash` is not tampered, we will utilize annoucement.
- The standard coin creates the launcher coin and assert the announcement from the same launcher coin that is spent at the same time. The launcher coin is an ephemeral coin.

### Standard Coin Spend Conditions
> Usually, the parent is going to be a standard coin. In the standard coin, we sign the puzzle that makes the conditions. If we create an `ASSERT_COIN_ANNOUNCEMENT` condition, we implicitly sign that too. -- [The Launcher](https://chialisp.com/docs/puzzles/singletons/#the-launcher)

- `launcher_coin_id` can be derived from the standard coin id which is the `parent_coin_id` and `launcher_puzzle_hash` and `amount`. 
- The standard coin asserts that there is an announcement from the **ephemeral launcher coin** with **the expected** `singleton_puzzle_hash`.

```lisp
(CREATE_COIN launcher_puzzle_hash)
(ASSERT_COIN_ANNOUNCEMENT sha256(launcher_coin_id + (sha256tree (singleton_full_puzzle_hash amount key_value_list))))
(AGG_SIG_ME owner_pubkey my_solution)
```
### Launcher Coin Spend Conditions
- `launcher_puzzle_reveal` is the [standard launcher](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/singleton_launcher.clvm). `solution` includes `singleton_puzzle_hash`, `amount`, and `key_value_list`.

> The last thing to note is the seemingly useless key_value_list that is passed in as an argument and announced. The purpose for this is to communicate information to blockchain observers. Sometimes you want to be able to know information about a puzzle before it is revealed. The only way we can get this information on chain is from the parent's puzzle reveal so sometimes it is useful to have useless parameters be part of the solution in order to make it easier to follow the puzzle's on chain state. Remember that you pay cost for every byte though so keep it concise.  -- [The Launcher](https://chialisp.com/docs/puzzles/singletons/#the-launcher)

```lisp
(CREATE_COIN singleton_full_puzzle_hash amount)
(CREATE_COIN_ANNOUNCEMENT (sha256tree (singleton_full_puzzle_hash amount key_value_list)))
```

> If the launcher coin doesn't create the coin with **the expected** `singleton_puzzle_hash`, the standard coin is not even spend and the launcher coin never exists!

### Singleton Coin

- The singleton code is actually a wrapper layer that modified the input to and output from the inner puzzle.

- The singleton layer guarantees uniqueness by verifying odd value mojo rule.
- The inner puzzle provides customized behavior.

#### 0. solution

```lisp
(list
    SINGLETON_STRUCT; (MOD_HASH . (LAUNCHER_ID . LAUNCHER_PUZZLE_HASH))
    INNER_PUZZLE
    lineage_proof
    my_amount
    inner_solution
)
```

##### `lineage_proof`
```lisp
(parent_parent_coin_info parent_inner_puzzle_hash parent_amount)
; or
(parent_parent_coin_info parent_amount) ; eve spend
```


```lisp
(defun-inline is_not_eve_proof (lineage_proof) (r (r lineage_proof)))
```

```sh
# not eve spend
❯ brun '(r (r 1))' '(0xdeadbeef 0xcafef00d 1_001)'
(1001)

# eve spend
❯ brun '(r (r 1))' '(0xdeadbeef 1_001)'
()
```



[singleton_top_layer_v1_1.clvm](https://github.com/Chia-Network/chia-blockchain/blob/optimize_singleton_v1.1/chia/wallet/puzzles/singleton_top_layer_v1_1.clvm)

#### 1. verify `my_amount` is an odd value

> `logand` (logand A B ...) bitwise AND of one or more atoms. Identity is -1.

> constant ONE == 1 (imported from [curry-and-treehash.clinc](https://github.com/Chia-Network/chia-blockchain/blob/optimize_singleton_v1.1/chia/wallet/puzzles/curry-and-treehash.clinc#L6))

```lisp
  ; main

  ; if our value is not an odd amount then we are invalid
  ; this calculates my_innerpuzhash and passes all values to stager_one
  (if (logand my_amount ONE)
    (stager_one SINGLETON_STRUCT lineage_proof (sha256tree1 INNER_PUZZLE) my_amount INNER_PUZZLE inner_solution)
    (x)
  )
```

#### 2. staggers

> The purpose of these functions is to calculate values that are used multiple times only once.

##### `stagger_one`
- calculate `full puzzle hash`

##### `stagger_two`
- calculate `coin ID`
    - if not an eve spend, create a new `coin ID`
    - if eve spend, verify `launcher ID` & `launcher puzzle hash`from the curried in `SINGLETON_STRUCT` are correct

```lisp
    ; SINGLETON_STRUCT = (MOD_HASH . (LAUNCHER_ID . LAUNCHER_PUZZLE_HASH))
    (defun-inline launcher_id_for_singleton_struct (SINGLETON_STRUCT)
        (f (r SINGLETON_STRUCT))
    )
    (defun-inline parent_info_for_lineage_proof (lineage_proof) (f lineage_proof))
    (defun-inline launcher_puzzle_hash_for_singleton_struct (SINGLETON_STRUCT)
        (r (r SINGLETON_STRUCT))
    )
    (defun-inline amount_for_lineage_proof (lineage_proof) (f (r (r lineage_proof))))

    (if (=
            (launcher_id_for_singleton_struct SINGLETON_STRUCT)
            (sha256 
                (parent_info_for_eve_proof lineage_proof) (launcher_puzzle_hash_for_singleton_struct SINGLETON_STRUCT) (amount_for_eve_proof lineage_proof)
            )
        )
            
        (sha256 (launcher_id_for_singleton_struct SINGLETON_STRUCT) full_puzhash my_amount)
        (x)
    )
```

> The first if statement checks if lineage_proof indicates that this is not the eve spend (three proof elements instead of two). If it is not the eve spend, it calculates our ID using the information in the `lineage_proof` to generate our `parent ID`.

> If it is the eve spend, there is an extra check which verifies that the launcher ID and launcher puzzle hash we have (both inside the SINGLETON_STRUCT) are correct. 

##### `stagger_three`
- generate conditions
    - `ASSERT_MY_COIN_ID my_coin_id` (make sure it's correct coin to be spent)
    - `check_and_morph_conditions_for_singleton` check the conditions generated from evaluation of `inner puzzle` and `inner solutions` for singleton specific things:
        - only one odd output
        - wrap the child singleton

#### Wrapped Puzzle Hash
It's very important to know that the puzzle hash from the inner puzzle will be updated (the new puzzle hash is called wrapped puzzle hash) by the singleton layer to be the new singleton coin. Also, the inner puzzle also should have no idea about being inside the singleton. 

#### Truths

The singleton layer already verify the followings:

- The coin's id
- The coin's puzzle hash
- The coin's inner puzzle hash
- The coin's amount
- The coin's lineage proof
- The coin's singleton information:
    - The singleton's code
    - The launcher's code 
    - The launcher's id

> The new Singleton 1.1 standard removed Truths because it was originally an optimization, but was causing headaches. [New Singleton 1.1 Standard Top Layer](https://developers.chia.net/t/new-singleton-1-1-standard-top-layer/387)

#### State

We can track the sington coin via launcher id and tracing the odd outputs every time it's spent on the blockchain. The idea is to store the state inside the inner puzzle of the singleton coin which is usually a puzzle hash that must be inferred.

Singleton also has key-value pairs in a list that can be secured with annoucement. We could observe the spend and check the solution.

#### Bonus
- Nested Inner Puzzles
- [Payment to Singletons](https://chialisp.com/docs/puzzles/singletons#pay-to-singleton)
    - We can make payments to singletons by creating a puzzle that knows the launcher ID of our singleton and requires an annoucement from our singleton in order to be spent.








- Stateful things like “which pool a miners plots are attached to” have to be represented with immutable “coins”. 
- The Plot NFT is actually a “coin” created by spending a the “singleton genesis coin”. 
- The “singleton genesis coin” is itself XCH (1 mojo) because all state in Chia is represented by unspent XCH coins. 
- When a miner spends this “singleton genesis coin”, it creates a singleton which specifies the pool it wants to participate in. 
- And if a miner wants to update its pool it would “spend” the singleton to create a new singleton. 
- Chia has recreated “state” in a clever and functionally pure way, but all the components and layers of indirection can be overwhelming.
- In Chia Lisp, you can compactly represent state using hash trees.

## Conclusions

To implement "state" in a coin set model, Chia has a singleton puzzle which can be used to wrap any puzzle while maintaining properties of pure functional programming paradigm like immutability (a new state is a new coin and not the update of the existing coin). 


# References

- [What is a singleton?](https://developers.chia.net/t/what-is-a-singleton/87)
- [Can you store state on the network?](https://developers.chia.net/t/can-you-store-state-on-the-network/84)
- [Singletons | Chialisp Docs](https://chialisp.com/docs/puzzles/singletons)
- [Singletons and Ethereum-like Contracts in Chia | Chialisp](https://www.youtube.com/watch?v=kA0l9n5SEI8)
- [Official Pooling Protocol Launched](https://www.chia.net/2021/07/07/official-pooling-launched.en.html)
- [Using the EVM to simplify Chia Pools](https://medium.com/liquidum-network/using-the-evm-to-simplify-chia-pools-d5bd696411c3)
- [New Singleton 1.1 Standard Top Layer](https://developers.chia.net/t/new-singleton-1-1-standard-top-layer/387)
- [singleton_top_layer.py](https://github.com/Chia-Network/chia-blockchain/blob/optimize_singleton_v1.1/chia/wallet/puzzles/singleton_top_layer.py)
- [`logand`](https://chialisp.com/docs/ref/clvm#bit-operations)

https://github.dev/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/singleton_top_layer.py
https://github.dev/Chia-Network/chia-blockchain/blob/optimize_singleton_v1.1/chia/wallet/puzzles/singleton_top_layer.py
https://github.com/Chia-Network/chia-blockchain/blob/main/tests/clvm/test_singletons.py
https://github.com/Flax-Network/flax-light-wallet/blob/94d3eede10f3feb3ec3cd3b783c168524b37c2b3/flaxlight/wallet/did_wallet/did_wallet_puzzles.py#L29
https://github.dev/Chia-Network/chia-blockchain/blob/optimize_singleton_v1.1/chia/wallet/puzzles/singleton_top_layer_v1_1.clvm
https://github.com/geoffwalmsley/CreatorNFT/blob/c5b818c03c9e31cfc629b05e4fad239cc1693397/tests/test_puzzles.py#L456