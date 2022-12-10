## Quote
> In most programming languages, evaluating a literal returns the value itself. **In CLVM, the meaning of an atom at evaluation time (at any position of the list except the first), is a reference to a value in the [argument tree](https://chialisp.com/clvm#environment).** -- [CLVM -- Quoting](https://chialisp.com/clvm#quoting-atoms)

> To interpret an **atom** as a **value**, rather than a **program**, it needs to be quoted with `q`. -- [CLVM -- Quote](https://chialisp.com/syntax#quoting)

```sh
# not quote
# 2 is (f (100 12)) => 100
# 5 is (f (r (100 12))) => (f (12)) => 12
❯ brun '(+ 2 5)' '(100 12)'
112

# quote 5 
❯ brun '(+ 2 (q . 5))' '(100 12)'
105

# quote both
❯ brun '(+ (q . 2) (q . 5))' '(100 12)'
7

# quote 1
❯ brun '(q . 1)' '(100)'
1

# (1) == (q), 1 is treated as operator q
❯ brun '(1 . 100)'
100
❯ brun '(1)' '(100)'
()
❯ brun '(q)'
()

# 1 is the whole solution (argument tree)
❯ brun '1' '(100)'
(100)

# chialisp doesn't need to quote
❯ run '(+ 2 5)'
7
❯ run '(list (q . 100) 100)'
(100 100)

```

```sh
# q . number (number is ignore), q is 1 which is the whole solution
❯ brun 'q . 5' '(100 100)'
(100 100)
❯ brun 'q . 1' '(100)'
(100)
❯ brun 'q . 2' '(100)'
(100)
❯ brun '2' '(2)'
2

❯ brun '(q . (100 . ()))'
(100)

❯ brun '(q 100)'         
(100)

❯ brun '(= (f (q 100)) (f (q . (100 . ()))))'
1
```

## `qq` and `unquote`
> `qq` allows us to quote something with selected portions being evaluated inside by using `unquote`. ... it allows us to substitute sections of predetermined code. -- [Chialisp -- Quote](https://chialisp.com/operators/#evaluation)

> `(qq EXPR)` for expanding templates. This is generally for creating your own operators that end up being inline functions. Everything in EXPR is quoted literally, unless it's wrapped by a unary `unquote` operator, in which case, it's **evaluated**. -- [`qq` and `unquote`](https://github.com/Chia-Network/clvm_tools#qq-and-unquote)

```sh
# evaluate
❯ run '(+ 5 (+ 1 2))'
8

# quote
❯ run '(q . (+ 5 (+ 1 2)))'
(+ 5 (+ 1 2))

## qq without unquote (no template to expand)
❯ run '(qq (+ 5 (+ 1 2)))'
(+ 5 (+ 1 2))

# qq and unquote
# (+ 1 2) is evaluated to 3
❯ run '(qq (+ 5 (unquote (+ 1 2))))'
(+ 5 3)
```