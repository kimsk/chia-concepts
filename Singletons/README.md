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
- DIDs () : A parent singleton can be treated as DID. [Mainnet Anniversary AMA](https://youtu.be/8tXkrMs1flg?t=3206), [ChiaLisp & Decentralized Identity](https://www.youtube.com/watch?v=zAG9KeMTZw8)


## How it works?

To ensure that the coin is unique, when a singleton coin is spent, it creates another singleton coin with the same launcher id. This, however, doesn't prevent a singleton coin to create non-singleton coins.

### Rules of Singleton
- A singleton must have an odd mojo value.
- Only one output (i.e., a singleton) coin can have an odd value.
- All singletons should have the same format.

### Bootstrapping

> We need to ensure that only one singleton is created with the same ID. This is surprisingly difficult. The crux of the issue is that we have no control over the coin that creates the singleton. 

> This is technically detectable by crawling up the chain and checking the first non-singleton coin to see if it had multiple singleton children, but this is inefficient and we would like all of our logic to be contained to the puzzles.

> Instead, what we can use is a launcher which is a specific puzzle that does exactly one thing: create a single singleton. We then need to curry this launcher puzzle hash into our singleton and have the first singleton assert that it, in fact, came from a parent whose puzzle hash was the launcher puzzle hash. Then, when people look at our singleton, they can see that the launcher puzzle hash is the hash of what they know to be a puzzle that creates only one singleton. They don't need to go back to the original parent and verify because the singleton puzzle takes care of that right from the start!
[The Launcher](https://chialisp.com/docs/puzzles/singletons#the-launcher)

- A first singleton coin must be created from the coin called **the Launcher** by passing in our `singleton_puzzle_hash` (as a solution).
- To make sure that the `singleton_puzzle_hash` is not tampered, we will utilize annoucement.
- The standard coin creates the launcher coin and assert the announcement from the same launcher coin that is spent at the same time. The launcher coin is an ephemeral coin.

`launcher_coin_id` can be derived from the standard coin id which is the `parent_coin_id` and `launcher_puzzle_hash` and `amount`. Then the standard coin can assert that there is an announcement from the ephemeral launcher coin with **the expected** `singleton_puzzle_hash`. If the launcher coin doesn't create the coin with **the expected** `singleton_puzzle_hash`, the standard coin is not even spend and the launcher coin never exists!

`launcher_puzzle_reveal` is the [standard launcher](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/singleton_launcher.clvm). `solution` includes `singleton_puzzle_hash`.


#### Standard Coin Spend Conditions
```lisp
(CREATE_COIN launcher_puzzle_hash)
(ASSERT_COIN_ANNOUNCEMENT sha256(launcher_coin_id + singleton_puzzle_hash))
(AGG_SIG_ME owner_pubkey my_solution)
```
#### Launcher Coin Spend Conditions
```lisp
(CREATE_COIN singleton_puzzle_hash)
(CREATE_COIN_ANNOUCEMENT singleton_puzzle_hash)
```

### Singleton Coin

- The singleton code is actually a wrapper layer that modified the input to and output from the inner puzzle.

- The singleton layer guarantees uniqueness by verifying odd value mojo rule.
- The inner puzzle provides customized behavior.

#### Wrapped Puzzle Hash
It's very important to know that the puzzle hash from the inner puzzle will be updated (the new puzzle hash is called wrapped puzzle hash) by the singleton layer to be the new singleton coin. Also, the inner puzzle also should have no idea about being inside the singleton. 

#### Truths










- Stateful things like “which pool a miners plots are attached to” have to be represented with immutable “coins”. 
- The Plot NFT is actually a “coin” created by spending a the “singleton genesis coin”. 
- The “singleton genesis coin” is itself XCH (1 mojo) because all state in Chia is represented by unspent XCH coins. 
- When a miner spends this “singleton genesis coin”, it creates a singleton which specifies the pool it wants to participate in. 
- And if a miner wants to update its pool it would “spend” the singleton to create a new singleton. 
- Chia has recreated “state” in a clever and functionally pure way, but all the components and layers of indirection can be overwhelming.
- In Chia Lisp, you can compactly represent state using hash trees.

## Conclusions

To implement "state" in a coin set model, Chia has a singleton puzzle which can be used to wrap any puzzle while maintaining properties of pure functional programming paradigm like immutability (a new state is a new coin and not the update of the existing coin). 


## References

- [What is a singleton?](https://developers.chia.net/t/what-is-a-singleton/87)
- [Can you store state on the network?](https://developers.chia.net/t/can-you-store-state-on-the-network/84)
- [Singletons | Chialisp Docs](https://chialisp.com/docs/puzzles/singletons)
- [Singletons and Ethereum-like Contracts in Chia | Chialisp](https://www.youtube.com/watch?v=kA0l9n5SEI8)
- [Official Pooling Protocol Launched](https://www.chia.net/2021/07/07/official-pooling-launched.en.html)
- [Using the EVM to simplify Chia Pools](https://medium.com/liquidum-network/using-the-evm-to-simplify-chia-pools-d5bd696411c3)