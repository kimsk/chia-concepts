# Counter

In this notebook, we create several puzzles to implement counter (0 to `MAX_COUNT`).

This exmple demostrates several Chia concepts and design patterns:
1. [Outer and Inner puzzles](https://chialisp.com/docs/common_functions#outer-and-inner-puzzles)
2. [Currying](https://chialisp.com/docs/common_functions#currying)
3. [Singleton](https://chialisp.com/docs/puzzles/singletons)
    - [notebook](https://github.com/kimsk/chia-concepts/blob/main/notebooks/intermediate/singleton/notebook.ipynb)
    - [singleton_top_layer_v1_1.clvm](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/singleton_top_layer_v1_1.clvm)
    - [singleton_top_layer_v1_1.py](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/singleton_top_layer_v1_1.py)
4. [Storing State](https://developers.chia.net/t/can-you-store-state-on-the-network/84)
    - Deriving current state from previous coin spend

### Counter Puzzle
#### [counter.clsp](counter.clsp)

This is the main puzzle storing the current count. When a coin with this puzzle is spent, a new coin with `count + 1` is created. A `TERMINAL_PUZZLE` can be provided to customize the output of the last coin (when `COUNT` is equal to the `MAX_COUNT`).  

```clojure
; MOD: the puzzle itself
; MAX_COUNT: maximum count
; TERMINAL_PUZZLE: an inner puzzle run when the count reach maximum
; AMOUNT: coin amount (odd for singleton)
; COUNT: current count

(mod (MOD MAX_COUNT TERMINAL_PUZZLE AMOUNT COUNT)
    (include condition_codes.clib)
    (include utils.clib)

    (defun create-next-counter (MOD MAX_COUNT TERMINAL_PUZZLE AMOUNT COUNT)
        (list
            (list CREATE_COIN 
                (sha256tree
                        (curry
                            MOD
                            (list
                                MOD MAX_COUNT TERMINAL_PUZZLE AMOUNT
                                (+ COUNT 1) ; increase count by one
                            )
                        )
                )
                AMOUNT
            )
        )
    )

    (if (= MAX_COUNT COUNT)
        (a TERMINAL_PUZZLE ()) ; Terminated
        (create-next-counter MOD MAX_COUNT TERMINAL_PUZZLE AMOUNT COUNT)
    )
)    
```

### Terminal Puzzle

The terminal puzzles are inner puzzles providing the terminal conditions for the counter puzzle. The `create-coin` puzzle will just create a new coin while the `terminate-singleton` puzzle will also provide `-113` which is a terminate signal for the standard [singleton top layer puzzle](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/singleton_top_layer_v1_1.clvm). 

#### [create-coin.clsp](create-coin.clsp)

```clojure
(mod (PUZZLE_HASH AMOUNT)
    (include condition_codes.clib)

    (list
        (list CREATE_COIN PUZZLE_HASH AMOUNT)
    )
)
```

#### [terminate-singleton.clsp](terminate-singleton.clsp)
```clojure
(mod (PUZZLE_HASH AMOUNT)
    (include condition_codes.clib)

    (list
        (list CREATE_COIN PUZZLE_HASH -113) ; terminate singleton
        (if (logand AMOUNT 1) ; create even amount
            (list CREATE_COIN PUZZLE_HASH (- AMOUNT 1)) 
            (list CREATE_COIN PUZZLE_HASH AMOUNT)
        )
    )
)
```

## Notebooks

See the working examples via the notebooks:

- [create-coin notebook](create-coin.ipynb)
- [singleton counter notebook](singleton-counter.ipynb)