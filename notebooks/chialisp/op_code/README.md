- [Map of Numberings](https://mojopuzzler.org/mediawiki/index.php/Map_of_Numberings)
- [Chia-Network//clvm/clvm/operators.py](https://github.com/Chia-Network/clvm/blob/main/clvm/operators.py#L25)
```python
    # core opcodes 0x01-x08
    ". q a i c f r l x "

    # opcodes on atoms as strings 0x09-0x0f
    "= >s sha256 substr strlen concat . "

    # opcodes on atoms as ints 0x10-0x17
    "+ - * / divmod > ash lsh "

    # opcodes on atoms as vectors of bools 0x18-0x1c
    "logand logior logxor lognot . "

    # opcodes for bls 1381 0x1d-0x1f
    "point_add pubkey_for_exp . "

    # bool opcodes 0x20-0x23
    "not any all . "

    # misc 0x24
    "softfork "
```

- [Chia-Network/clvm_rs/src/chia_dialect.rs](https://github.com/Chia-Network/clvm_rs/blob/main/src/chia_dialect.rs#L47)
```rust
        let f = match b[0] {
            3 => op_if,
            4 => op_cons,
            5 => op_first,
            6 => op_rest,
            7 => op_listp,
            8 => op_raise,
            9 => op_eq,
            10 => op_gr_bytes,
            11 => op_sha256,
            12 => op_substr,
            13 => op_strlen,
            14 => op_concat,
            // 15 ---
            16 => op_add,
            17 => op_subtract,
            18 => op_multiply,
            19 => {
                if (self.flags & NO_NEG_DIV) != 0 {
                    op_div_deprecated
                } else {
                    op_div
                }
            }
            20 => op_divmod,
            21 => op_gr,
            22 => op_ash,
            23 => op_lsh,
            24 => op_logand,
            25 => op_logior,
            26 => op_logxor,
            27 => op_lognot,
            // 28 ---
            29 => op_point_add,
            30 => op_pubkey_for_exp,
            // 31 ---
            32 => op_not,
            33 => op_any,
            34 => op_all,
            // 35 ---
            36 => op_softfork,
            _ => {
                if (self.flags & NO_UNKNOWN_OPS) != 0 {
                    return err(o, "unimplemented operator");
                } else {
                    return op_unknown(allocator, o, argument_list, max_cost);
                }
            }
        };
        ...
        fn quote_kw(&self) -> &[u8] {
            &[1]
        }

        fn apply_kw(&self) -> &[u8] {
            &[2]
        }
```