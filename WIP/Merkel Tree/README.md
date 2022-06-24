- [Merkle Tree in Blockchain: What is it, How does it work and Benefits](https://www.simplilearn.com/tutorials/blockchain-tutorial/merkle-tree-in-blockchain)


> Coin set uses two Merkle trees (one for inputs and one for outputs), which allows all transactions in a block to occur simultaneously. As long as all of the inputs are unspent (coins can only be spent once) and all of the values are valid (you can't create more than you burn, for example), the transactions will be valid. This is one of the differences between coin set and UTXO, which only uses a single Merkle tree for inputs and outputs. -- [keybase](keybase://chat/chia_offers#general/1662)

> In Bitcoin's UTXO model, an individual block's transactions are organized as a Merkle tree, where each transaction in a block is a leaf, and the coinbase transaction is the root. The leaves must be sorted in topological, or natural, order. If transaction B spends an output of transaction A, then both A and B are allowed to occur in the same block, but A must be stored in an earlier position than B in the Merkle tree.

> In Chia's coin set model, each of a block's transactions occur simultaneously. Chia uses two Merkle trees – one for removing coins, and one for adding them. -- [Transaction/coin processing](https://docs.chia.net/docs/04coin-set-model/coin_set_vs_utxo/#transactioncoin-processing)