# เกม ทิก-แทก-โท

ในตัวอย่างนี้เราจะมาสร้า[เกมทิก-แทก-โท](https://en.wikipedia.org/wiki/Tic-tac-toe) บน Chia บล็อกเชนโดยใช้ Coin Set Model และ Chialisp

```
 
         x | o | x              x | o | x 
        ---+---+---            ---+---+---
           | o | x        =>      | o | x 
        ---+---+---            ---+---+---
           |   |                x |   |   

```

## แนวคิดและ Design Patterns

ตัวอย่างนี้คล้ายๆกับ [counter](../counter/README.md) ที่นำแนวคิดและ Design Patterns มาใช้

### 1. [Outer and Inner Puzzles](https://chialisp.com/docs/common_functions#outer-and-inner-puzzles)

> Outer and Inner Puzzle เป็น design pattern ที่ส่งเสริมแนวปฏิบัติการสร้างซอฟต์แวร์ที่ดีเช่น [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns), [composition](https://en.wikipedia.org/wiki/Object_composition), and [unit testings](https://en.wikipedia.org/wiki/Unit_testing)

> งานของ [singleton top layer puzzle](https://github.com/kimsk/chia-concepts/blob/main/notebooks/intermediate/singleton/notebook.ipynb) คือการควบคุม[กฎของ singleton](https://github.com/kimsk/chia-concepts/blob/main/notebooks/intermediate/singleton/notebook.ipynb) เท่านั้น ในขณะที่ [tic tac toe coin puzzle](https://github.com/kimsk/chia-concepts/blob/main/notebooks/misc/tic-tac-toe/code/coin.clsp) ก็ไม่จำเป็นต้องรู้ด้วยว่าตัวมันเองถูกใช้ใน singlton top layer puzzle อีกที

> [tic tac toe puzzle](https://github.com/kimsk/chia-concepts/blob/main/notebooks/misc/tic-tac-toe/code/tic-tac-toe.clsp) ไม่จำเป็นต้องรู้ว่ากำลังถูกใช้โดย puzzle อื่นหรือกำงานด้วยตัวมันเอง

> เราสามารถเลือกใช้ [terminate game puzzle](https://github.com/kimsk/chia-concepts/blob/main/notebooks/misc/tic-tac-toe/code/terminate-game.clsp) ให้เหมาะกับสถานการ์ณ เช่น ถ้าเราต้องการใช้ [tic tac toe coin puzzle](https://github.com/kimsk/chia-concepts/blob/main/notebooks/misc/tic-tac-toe/code/coin.clsp) กับ [singleton top layer puzzle](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/puzzles/singleton_top_layer_v1_1.clvm#L55) เราจำเป็นต้องใช้ terminate game puzzle ที่สามารถสร้าง `CREATE_COIN 0x... -113` เพื่อที่จะหลอมเหรียญ singleton 

> แนวคิดนี้มีพื้นฐานเดียวกันกับ [Dependency injection design pattern](https://en.wikipedia.org/wiki/Dependency_injection)

```
    +---------------------+
    | singleton top layer |
    |-+-------------------+
    | | tic tac toe coin  |
    | |-+-----------------+
    | | | tic tac toe     |
    | | | terminate game  |
    +---------------------+
```

![singleton-tic-tac-toe](singleton-tic-tac-toe.jpg)

### 2. [Currying](https://chialisp.com/docs/common_functions#currying)

#### Pre-commit Environment and Store State
> เราสามารถปรับเปลี่ยน puzzle ให้เหมาะกับสถานการณ์ต่างๆกันไปโดยใช้ Currying

> Chialisp เป็น pure functional programming language ซึ่งหมายความว่าโปรแกรมที่เขียนโดย Chialisp จะทำงานกับค่าที่ถูกส่งเข้ามาในฟังก์ชั่นโดยตรง 

> ในเกม tic tac toe เราเก็บบอร์ดและตาที่จะเล่น (`x` หรือ `o`) ลงใน puzzle โดยใช้ currying เพราะฉะนั้นการรันโปรแกรมเราแค่ผ่านตำแหน่งที่ต้องการเท่านั้น

```lisp
;   BOARD : current tic tac toe board state (curried)
;   V     : x or o to be played (curried)
;   pos   : position to be played
(mod (BOARD V pos)
    (include tic-tac-toe.clib)

    (defun play (new_board V)
        (list 
            (check-board new_board V)
            new_board
        )
    )

    ; 1. get new board
    ; 2. return the play result and new board
    (play (get-new-board BOARD V pos) V)
)
```

> หลังจากที่ curry ค่าที่ต้องการเราสามารถนำ puzzle ไป curry ต่อ และคำนวณ puzzle hash สำหรับเหรียญใหม่ได้ดังนี้

```lisp
(create-new-coin
    ; puzzle_hash
    (sha256tree
        (curry
            MOD
            (list
                MOD
                TERMINATE_PUZZLE
                (list PLAYER_ONE_PK PLAYER_ONE_HASH)
                (list PLAYER_TWO_PK PLAYER_TWO_HASH)
                (curry
                    tic_tac_toe_puzzle 
                    (list 
                        next_board
                        next_player
                    )
                )
                AMOUNT
            )
        )
    )
    AMOUNT
)
```

### 3. [Storing and Retrieving State](https://developers.chia.net/t/can-you-store-state-on-the-network/84)

> From the curried puzzle, we could extract the curried values representing state that we want.

```lisp
(defun-inline get-player-from-curried-tic-tac-toe-puzzle (curried_puzzle)
    (r (f (r (f (r (r (f (r (r curried_puzzle)))))))))
)
```