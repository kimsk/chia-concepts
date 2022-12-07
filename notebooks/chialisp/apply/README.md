- [Evaluation](https://chialisp.com/operators#evaluation)
- [Rigidity/clvm](https://github.com/Rigidity/clvm/blob/main/test/run.ts#L48)

```sh
❯ brun '(a (q . 1) (q . 100))'       
100

❯ brun '1' '100'
100

❯ brun '(a (q . (+ 1 1)) (q . 100))' 
200

❯ brun '(+ 1 1)' '100'
200

❯ cdv clsp curry ./map.clsp -a '(+ 1 1)'
(a (q 2 (q 2 2 (c 2 (c 5 (c 7 ())))) (c (q 2 (i 11 (q 4 (a 5 19) (a 2 (c 2 (c 5 (c 27 ()))))) ()) 1) 1)) (c (q 16 1 1) 1))

❯ brun '(a (q . (a (q 2 (q 2 2 (c 2 (c 5 (c 7 ())))) (c (q 2 (i 11 (q 4 (a 5 19) (a 2 (c 2 (c 5 (c 27 ()))))) ()) 1) 1)) (c (q 16 1 1) 1))) (q . (100 200 300)))'
(200 400 600)

```