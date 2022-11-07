
## Notebooks
- [Standard Transactions](./standard-txn.ipynb)
- [Synthetic Keys](./synthetic-keys.ipynb)

## Scenarios
1. [Normal Spend](code/normal-spend.py)
    - `DEFAULT_HIDDEN_PUZZLE_HASH`
    - alice is the coin owner and wants to send coin to bob
    
1. [Approved Spend (2 of 2)](code/approved-spend.py)
    - `DEFAULT_HIDDEN_PUZZLE_HASH`
    - alice is the coin owner (i.e., coin's puzzle hash encoded to alice's wallet address & changes return to alice).
    - alice wants to send xch to charlie.
    - bob needs to **approve** the amount and recipient's address.

1. [Multi-sig (m of m)](code/multi-sig-m-of-m.py)
    - `DEFAULT_HIDDEN_PUZZLE_HASH`
    - alice, bob, and charlie wants to contribute 1 XCH each (total of 3 XCH) and give to dan.
    - everyone has to contribute or the spend won't happen. 
    
1. Saving Coin
    - alice and bob has a child named charlie.
    - alice and bob wants to save 2 XCH for charlie.
    - both alice and bob has to sign to spend the saving coin.
    1. [Saving Coin (Custom Puzzle)](code/scenario-1.py)
    1. [Saving Coin (Standard Transaction + Hidden Puzzle)](code/scenario-1-hidden-puzzle.py)

1. Others
    - [spend_coin_sim.py](code/spend_coin_sim.py)
    > alice sends xch to bob.

    - [spend_coin_testnet10.py](code/spend_coin_testnet10.py)
    > send random coin on testnet10

## References
- [Aggregated Signatures, Taproot, Graftroot, and Standard Transactions](https://www.chia.net/2021/05/27/Agrgregated-Sigs-Taproot-Graftroot.html)
- [Standard Transactions](https://chialisp.com/standard-transactions)
- [Signatures in Chia](https://aggsig.me/signatures.html)
- [What is Taproot? Technology to Enhance Bitcoin’s Privacy](https://blockonomi.com/bitcoin-taproot/)
- [What is Bitcoin’s Graftroot? Complete Beginner’s Guide](https://blockonomi.com/bitcoin-graftroot/)
- [Multi-signature application examples](https://en.bitcoin.it/wiki/Multi-signature)