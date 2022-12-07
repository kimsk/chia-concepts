- [clvm_tools_rs](https://github.com/prozacchiwawa/clvm_tools_rs)
```
src/classic  <-- any ported code with heritage pointing back to
                 the original chia repo.
                
src/compiler <-- a newer compiler (ochialisp) with a simpler
                 structure.  Select new style compilation by
                 including a `(include *standard-cl-21*)`
                 form in your toplevel `mod` form.
```

- [ochialisp](https://github.com/prozacchiwawa/ochialisp)


```sh
❯ run '(mod (x y) (+ x y))'                                            
(+ 2 5)

~ 
❯ run '(mod (x y) (include *standard-cl-21*) (+ x y))'                 
(2 (1 16 5 11) (4 (1) 1))

~ 
❯ brun (run '(mod (x y) (+ x y))') '(30 12)'                           
42

~ 
❯ brun (run '(mod (x y) (include *standard-cl-21*) (+ x y))') '(30 12)'
42
```

```clojure
(2 (1 16 5 11) (4 (1) 1))
```
```clojure
(a (q + 5 11) (q (1) 1))
```

```sh
❯ brun '(a (q + 5 11) (c (1) 1))' '(30 12)'
42

❯ brun '(a (q + 5 11) (c (q . (30 12)) (q . (30 12))))'
42

❯ brun '(c (q . (30 12)) (q . (30 12))))'                             
((pubkey_for_exp 12) 30 12)

# 30 is pubkey_for_exp
❯ brun '(a (q + 5 11) (q . ((30 12) 30 12)))'
42

# 5 is (f (r 1)) 
❯ brun '5' '((30 12) 30 12)'
30

# 11 is (f (r (r 1)))
❯ brun '11' '((30 12) 30 12)' 
12


```