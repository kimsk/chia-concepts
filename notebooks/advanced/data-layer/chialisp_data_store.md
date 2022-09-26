## Data

``` PowerShell
❯ Get-Content $ch21 | bat --language clojure
❯ Get-Content $ch21 | xxd -ps -c ($ch21.Length * 2)
❯ Get-Content $ch21 | xxd -ps -c ($ch21.Length * 2) | xxd -p -r | bat --language lisp
❯ Get-Content $ch21 | xxd -ps -c ($ch21.Length * 2) | xxd -p -r | tr -d "\n" | Edit-DoubleToSingleQuote
❯ brun '(r (f 1))' (Get-Content $ch21 | xxd -ps -c ($ch21.Length * 2) | xxd -p -r | tr -d "\n" | Edit-DoubleToSingleQuote)
("Chia Holiday 2021")
```

``` PowerShell
❯ "Chia Holiday 2021" | xxd -ps
4368696120486f6c6964617920323032310a

❯ chia rpc data_layer get_value (@{ id = $store_id; key = "0x4368696120486f6c6964617920323032310a" } | ConvertTo-ChiaRpcJson) `
∙ | jq ".value" `
∙ | xxd -p -r `
∙ | bat --language lisp

```
