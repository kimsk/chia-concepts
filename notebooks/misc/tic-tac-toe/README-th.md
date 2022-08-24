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