- [The power of Python Map, Reduce and Filter – Functional Programming for Data Science](https://www.analyticsvidhya.com/blog/2021/09/the-power-of-python-map-reduce-and-filter-functional-programming-for-data-science/)
- [The Holy Trinity of Functional Programming: Map, Filter and Reduce](https://dev.to/mlevkov/the-holy-trinity-map-filter-and-reduce-381e)

## Map
```clojure
(mod (FN . input_list)
    (defun rec (FN lst)
        (if lst
            (c
                (a FN (f lst))
               (rec FN (r lst))
            )
            lst
        )
    )
    (rec FN input_list)
)
```

```sh
# double
❯ brun (cdv clsp curry ./map.clsp -a '(+ 1 1)') '(42 72 37 53)' -c -y main.sym
cost = 8815
(84 144 74 106)

("rec" (+ 1 1) (42 72 37 53)) => (84 144 74 106)
("rec" (+ 1 1) (72 37 53)) => (144 74 106)
("rec" (+ 1 1) (37 53)) => (74 106)
("rec" (+ 1 1) (53)) => (106)
("rec" (+ 1 1) ()) => ()

# squre
❯ brun (cdv clsp curry ./map.clsp -a '(* 1 1)') '(42 72 37 53)' -c -y main.sym 
cost = 9821
(1764 5184 1369 2809)

("rec" (* 1 1) (42 72 37 53)) => (1764 5184 1369 2809)
("rec" (* 1 1) (72 37 53)) => (5184 1369 2809)
("rec" (* 1 1) (37 53)) => (1369 2809)
("rec" (* 1 1) (53)) => (2809)
("rec" (* 1 1) ()) => ()
```

## Reduce
```clojure
(mod (FN . input_list)
    (defun rec (FN acc lst)
        (if lst
            (rec FN
                (a FN (list acc (f lst)))
                (r lst)
            )
            acc
        )
    )
    (rec FN
        (f input_list) 
        (r input_list)
    )
)
```

```sh
# sum
❯ brun (cdv clsp curry ./reduce.clsp -a '(+ 2 5)') '(1 2 3 4 5)' -c -y main.sym 
cost = 9716
15

("rec" (+ 2 5) 1 (a 3 4 5)) => 15
("rec" (+ 2 5) 3 (i 4 5)) => 15
("rec" (+ 2 5) 6 (c 5)) => 15
("rec" (+ 2 5) 10 (f)) => 15
("rec" (+ 2 5) 15 ()) => 15

# factorial
❯ brun (cdv clsp curry ./reduce.clsp -a '(* 2 5)') '(1 2 3 4 5)' -c -y main.sym 
cost = 10692
120

("rec" (* 2 5) 1 (a 3 4 5)) => 120
("rec" (* 2 5) 2 (i 4 5)) => 120
("rec" (* 2 5) 6 (c 5)) => 120
("rec" (* 2 5) 24 (f)) => 120
("rec" (* 2 5) 120 ()) => 120
```

## Filter

```clojure
(mod (FN . input_list)
    (defun rec (FN acc lst)
        (if lst
            (rec FN
                (if (a FN (f lst))
                    (c
                        (f lst)
                        acc
                    )
                    acc
                )
                (r lst) 
            )
            acc
        )
    )

    (defun rev (acc lst)
        (if lst
            (rev (c (f lst) acc) (r lst))
            acc
        )
    )

    (rev
        ()
        (rec FN () input_list)
    )
)
```

```sh
❯ brun (cdv clsp curry ./filter.clsp -a '(> 1 (q . 42))') '(112 37 130 41 45)' -c -y main.sym
cost = 14403
(112 130 45)

("rec" (> 1 (q . 42)) () (112 37 130 41 45)) => (45 130 112)
("rec" (> 1 (q . 42)) (112) (37 130 41 45)) => (45 130 112)
("rec" (> 1 (q . 42)) (112) (130 41 45)) => (45 130 112)
("rec" (> 1 (q . 42)) (130 112) (41 45)) => (45 130 112)
("rec" (> 1 (q . 42)) (130 112) (45)) => (45 130 112)
("rec" (> 1 (q . 42)) (45 130 112) ()) => (45 130 112)

("rev" () (45 130 112)) => (112 130 45)
("rev" (45) (130 112)) => (112 130 45)
("rev" (130 45) (112)) => (112 130 45)
("rev" (112 130 45) ()) => (112 130 45)
```



## Map & Reduce

