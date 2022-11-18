# The Standard Transaction

To output the spend conditions, we can write chialisp puzzles to creates the conditions. However, [the puzzle could also be provided the conditions as solution to output as well](https://chialisp.com/docs/coins_spends_and_wallets#generating-conditions-from-the-puzzle-vs-from-the-solution).

Here is the simplest example:

``` lisp
(mod conditions
    conditions
)
```

``` sh
❯ brun (run '(mod conditions conditions)') '((51 0xcafef00d 1000) (73 1000))'      
((51 0xcafef00d 1000) (73 1000))
```

## Delegated Puzzle

Better yet, Chialisp puzzle, treating code (as a 1st class citizen) like data, can be provided [a puzzle and solution to execute](https://chialisp.com/docs/coins_spends_and_wallets#example-pay-to-delegated-puzzle) and output the conditions! 

We call the provided puzzle that can create the ouput conditions, [delegated puzzle](https://chialisp.com/docs/standard_transaction#pay-to-delegated-puzzle-or-hidden-puzzle).

Here is the simplest example:

```lisp
(mod (delegated_puzzle solution)
    (a delegated_puzzle solution)
)
```

Let's pass the simplest puzzle above:

```sh
# the delegated puzzle
❯ run '(mod conditions conditions)'                                                
1

# the delegaged puzzle is the 1st parameter
# the solution for the delegated puzzle is the 2nd parameter
❯ brun (run '(mod (delegated_puzzle solution) (a delegated_puzzle solution))') '(1 ((51 0xcafef00d 1000) (73 1000)))'
((51 0xcafef00d 1000) (73 1000))
```

## AGG_SIG_ME

But as we know, the puzzle is not secure if there is no `AGG_SIG_ME` in the list of conditions. Also, we will need to have **public key** available too if we want to include `AGG_SIG_ME` condition.

Here is the version with `AGG_SIG_ME`:

[simple_pay_to_delegated.clsp](simple_pay_to_delegated.clsp)
```lisp
(mod (PUB_KEY delegated_puzzle solution)

    (include condition_codes.clib)

    (c
        ; hard-coded message
        (list AGG_SIG_ME PUB_KEY (sha256 "hello delegated puzzle"))
        (a delegated_puzzle solution)
    )
)
```

[simple_pay_to_delegated.py](simple_pay_to_delegated.py)
```python
...

MOD = load_clvm("simple_pay_to_delegated.clsp", package_or_requirement=__name__, search_paths=["../include"])

# create a smart coin and curry in alice's pk
amt = 1_000_000
alice_mod = MOD.curry(alice.pk())
alice_coin = asyncio.run(
    alice.launch_smart_coin(
        alice_mod,
        amt=amt
    )
)

# (delegated_puzzle solution)
solution = Program.to([
    1, # (mod conditions conditions)
    [
        [ConditionOpcode.CREATE_COIN, bob.puzzle_hash, amt],
        [ConditionOpcode.ASSERT_MY_AMOUNT, alice_coin.amount]
    ]
])

# create a spend bundle with alice's signature
spend = CoinSpend(
    alice_coin.as_coin(),
    alice_mod,
    solution 
)

# hard-coded message
message: bytes = std_hash(bytes("hello delegated puzzle", "utf-8"))
alice_sk: PrivateKey = alice.pk_to_sk(alice.pk())
sig: G2Element = AugSchemeMPL.sign(
    alice_sk,
    message
    + alice_coin.name()
    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
)

spend_bundle = SpendBundle([spend], sig)
```

Running the simulation:

```sh
❯ python3 ./simple_pay_to_delegated.py
alice balance:  2000000000000
alice smart coin:       {'amount': 1000000,
 'parent_coin_info': '0x8d011a3236082916e08a2214379a063b38a8c7c2ed7fb6a708acf824e1d9b310',
 'puzzle_hash': '0x1a54f0b830d632b8ccbbf8ce0202489ce9312aad6f407c1ddb21def66e763345'}

push spend bundle:
{'aggregated_signature': '0x8a1fe76f86f45975bad21b38ab759675300f04c02be911b572d66270e56d1c87ddb9255bbaeca646f72e97d94e1737d0169130ee2c9038a154fe15fdc6218f36e30deaf4a00914659156dc91f68e6ceae3cbdc9c9ee182e19b04f3f082d08c92',
 'coin_spends': [{'coin': {'amount': 1000000,
                           'parent_coin_info': '0x8d011a3236082916e08a2214379a063b38a8c7c2ed7fb6a708acf824e1d9b310',
                           'puzzle_hash': '0x1a54f0b830d632b8ccbbf8ce0202489ce9312aad6f407c1ddb21def66e763345'},
                  'puzzle_reveal': '0xff02ffff01ff02ffff01ff04ffff04ff02ffff04ff05ffff01ffa011e82913276355e092ff40373677de4a87461938fb975e02b0ffe08fb3d88ba9808080ffff02ff0bff178080ffff04ffff0132ff018080ffff04ffff01b0ac2f40f6cb161f872f61910bdacd811534e5b5753242553d9022906cdfa479e172b1eac8e1f38a3743b7897e58942442ff018080',
                  'solution': '0xff01ffffff33ffa05abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6ff830f424080ffff49ff830f4240808080'}]}

alice balance:  1999999000000
bob balance:    1000000
```

## Sign Delegated Puzzle Hash

The above example is not secure because the malicious actor can modify the delegated puzzle and solution. _We could fix this by signing the hash of the delegated puzzle, so we are certain that nobody changes the delegated puzzle_.

```lisp
(c
    ; check if the delegated puzzle is tampered
    (list AGG_SIG_ME PUB_KEY (sha256tree delegated_puzzle))
    (a delegated_puzzle solution)
)
```

```python
 # message is a tree hash of `(mod conditions conditions)`
message: bytes = Program.to(1).get_tree_hash()
alice_sk: PrivateKey = alice.pk_to_sk(alice.pk())
sig: G2Element = AugSchemeMPL.sign(
    alice_sk,
    message
    + alice_coin.name()
    + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA,
)
```

The python code above shows how we pre-committed the delegated puzzle, `1` or `(mod conditions conditions)` without storing it inside the coin puzzle. We verify that the provided `delegated_puzzle` matches the expected puzzle by verifying the puzzle hash using `AGG_SIG_ME`.

## Pre-Committed Delegated Puzzle

We could also create a coin with pre-committed delegated puzzle and we just need solution to spend it.

### coin puzzle (password-locked-curried.clsp)
```lisp
(mod (PUZZLE PUB_KEY solution)
    (include condition_codes.clib)
    (include sha256tree.clib)
    (c
        (list AGG_SIG_ME PUB_KEY (sha256tree PUZZLE))
        (a PUZZLE solution)
    )
)
```

### password locked delegated puzzle (password-locked-delegated.clsp)
```lisp
; password is hard-coded, "hello"
(mod (password new_puzhash amount)
    (if (= (sha256 password) (q . 0x2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824))
            (list (list 51 new_puzhash amount))
            (x "wrong password")
    )
)
```

### run the simulator
```python
password_locked_delegated = load_clvm("password-locked-delegated.clsp", package_or_requirement=__name__, search_paths=["../include"]) 
password_locked_curried =  load_clvm(
        "password-locked-curried.clsp", package_or_requirement=__name__, search_paths=["../include"]
    ).curry(password_locked_delegated, alice.pk_) # curry PUZZLE and PUB_KEY

print(password_locked_curried) 

amt = 1_000_000_000
password_locked_curried_coin = launch_smart_coin(
    alice, 
    password_locked_curried, 
    amt)

password_locked_curried_coin_solution = Program.to([ 
    ["hello", bob.puzzle_hash, amt]
])

# sign the tree hash of password-locked-delegated puzzle
sig = AugSchemeMPL.sign(alice.sk_,
    (
        password_locked_delegated.get_tree_hash()
        + password_locked_curried_coin.name()
        + DEFAULT_CONSTANTS.AGG_SIG_ME_ADDITIONAL_DATA
    )
)

spend_bundle = SpendBundle(
    [
        CoinSpend(
            password_locked_curried_coin.as_coin(),
            password_locked_curried,
            password_locked_curried_coin_solution,
        )
    ],
    sig,
)
```

```json
{
    "aggregated_signature": "0xa46145ff038ae33d5776901c1a3dd36579ee6afda16cdb80a1ddaf4078b0a00703156c259bd1190dd321a25a7574946a057111aa4f0d9921dad7a3e6049e81bda1a8822439d885dfd7f9bb4e97a21489a7a9bf8b4a1e48919b4aa8c41ef6b6bd",
    "coin_spends": [
        {
            "coin": {
                "amount": 1000000000,
                "parent_coin_info": "0x8d011a3236082916e08a2214379a063b38a8c7c2ed7fb6a708acf824e1d9b310",
                "puzzle_hash": "0x1a45826b53cf0f3d759f664aad8e2303796284ecd59dbc78cb72cbc113dbd711"
            },
            "puzzle_reveal": "0xff02ffff01ff02ffff01ff04ffff04ff04ffff04ff0bffff04ffff02ff06ffff04ff02ffff04ff05ff80808080ff80808080ffff02ff05ff178080ffff04ffff01ff32ff02ffff03ffff07ff0580ffff01ff0bffff0102ffff02ff06ffff04ff02ffff04ff09ff80808080ffff02ff06ffff04ff02ffff04ff0dff8080808080ffff01ff0bffff0101ff058080ff0180ff018080ffff04ffff01ff02ffff03ffff09ffff0bff0280ffff01a02cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b982480ffff01ff04ffff04ffff0133ffff04ff05ffff04ff0bff80808080ff8080ffff01ff08ffff018e77726f6e672070617373776f72648080ff0180ffff04ffff01b0ac2f40f6cb161f872f61910bdacd811534e5b5753242553d9022906cdfa479e172b1eac8e1f38a3743b7897e58942442ff01808080",
            "solution": "0xffff8568656c6c6fffa05abb5d5568b4a7411dd97b3356cfedfac09b5fb35621a7fa29ab9b59dc905fb6ff843b9aca008080"
        }
    ]
}
```

## Pay To Delegated Puzzle or Hidden Puzzle

Chia team provides and recommmends utilizing a **standard transaction** with [Pay to "Delegated Puzzle" or "Hidden Puzzle"](https://chialisp.com/docs/standard_transaction#pay-to-delegated-puzzle-or-hidden-puzzle) for most vanilla transactions. Coins with the [puzzle](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.clvm) can be unlocked by either signing a delegated puzzle and its solution with a **synthetic private key** OR by **revealing the hidden puzzle and the underlying original key**.

The puzzle of normal coins you see in your wallet are the standard puzzle. If you look at the signature of the puzzle, you will see that `SYNTHETIC_PUBLIC_KEY` has to be curried in.

```lisp
(SYNTHETIC_PUBLIC_KEY public_key delegated_puzzle solution)
```
### Synthetic Key

The synthetic key is the key derived from:
1. the hidden puzzle itself.
2. the public key that can sign for the delegated spend case.

`synthetic_offset == sha256(hidden_puzzle_hash + public_key)`

`synthetic_public_key == public_key + synthetic_offset_pubkey`

![Taproot Public Key Generation](https://www.chia.net/assets/blog/Taproot-Pub-Key-Generation.png)
> The image is from [Aggregated Signatures, Taproot, Graftroot, and Standard Transactions](https://www.chia.net/2021/05/27/Agrgregated-Sigs-Taproot-Graftroot.html)

There are two ways to spend the standard transaction:

1. Signing a delegated puzzle and its solution with `synthetic_private_key`

```lisp
(SYNTHETIC_PUBLIC_KEY _public_key delegated_puzzle solution)
...

(c
    (list AGG_SIG_ME SYNTHETIC_PUBLIC_KEY (sha256tree1 delegated_puzzle)) 
    (a delegated_puzzle solution)
)
```
2. Revealing BOTH the **hidden puzzle** and the **public key**, so the standard transaction puzzle can derive the **synthetic public key** and make sure that it matches the one that is curried in.

```lisp
(SYNTHETIC_PUBLIC_KEY public_key hidden_puzzle solution)
...
(if (=
        SYNTHETIC_PUBLIC_KEY
        (point_add ; synthetic_public_key == public_key + synthetic_offset_pubkey
            public_key
            (pubkey_for_exp ( ; derive public key offset from synthetic_offset 
                    ; synthetic_offset == sha256(hidden_puzzle_hash + public_key)
                    sha256 public_key (sha256tree1 hidden_puzzle)
                )
            )
        )
    )
    (a hidden_puzzle solution)
    (x)
)
```

## Spend Standard Transaction

> p2_delegated_puzzle_or_hidden_puzzle is essentially the "standard coin" in chia. DEFAULT_HIDDEN_PUZZLE_HASH from this puzzle is used with
calculate_synthetic_secret_key in the wallet's standard pk_to_sk finder. [*](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.py#L18)

The cool thing about the standard transaction is that we can control how the standard transaction coin is spent by providing our own delegated puzzle and solutions. Or we could also pre-commit the hidden puzzle and spend later as well.

Let's look at some scenarios that we can use the `p2_delegated_puzzle_or_hidden_puzzle`.

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

## Conclusions

As you can see, the standard transaction puzzle is very flexible because we can provide `delegated puzzle` or `pre-committed puzzle` and `solution` that returns any `conditions`. It also introduces `synthetic keys` which better hide how the puzzle run.

## References

- [Aggregated Signatures, Taproot, Graftroot, and Standard Transactions](https://www.chia.net/2021/05/27/Agrgregated-Sigs-Taproot-Graftroot.html)- [2 - Coins, Spends and Wallets | Chialisp.com](https://chialisp.com/docs/coins_spends_and_wallets/)
- [3 - Deeper into CLVM | Chialisp.com](https://chialisp.com/docs/deeper_into_clvm/)
- [6 - The Standard Transaction | Chialisp.com](https://chialisp.com/docs/standard_transaction/)
- [Signatures in Chia](https://aggsig.me/signatures.html)
- [chia.wallet.puzzles.p2_delegated_puzzle_or_hidden_puzzle](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/p2_delegated_puzzle_or_hidden_puzzle.py)
- [What is Taproot? Technology to Enhance Bitcoin’s Privacy](https://blockonomi.com/bitcoin-taproot/)
- [What is Bitcoin’s Graftroot? Complete Beginner’s Guide](https://blockonomi.com/bitcoin-graftroot/)
- [Multi-signature application examples](https://en.bitcoin.it/wiki/Multi-signature)
