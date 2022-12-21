# Decentralized Identifier (DID)

`"did:" method-name ":" method-specific-id`
## Chia DID
`did:chia:10hq8mukapz8lml97tgnnsfdv24t9u5mw6pnqfh64kwh6vljykyrsc4m38t`

```sh
❯ cdv decode did:chia:10hq8mukapz8lml97tgnnsfdv24t9u5mw6pnqfh64kwh6vljykyrsc4m38t
7dc07df2dd088ffdfcbe5a273825ac55565e536ed06604df55b3afa67e44b107
```
`7dc07df2dd088ffdfcbe5a273825ac55565e536ed06604df55b3afa67e44b107` is a launcher coin name (e.g., coin id).

https://twitter.com/kimsk/status/1566728274893742083
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">gm <a href="https://twitter.com/hashtag/chialisper?src=hash&amp;ref_src=twsrc%5Etfw">#chialisper</a> <br>Fun Facts about <a href="https://twitter.com/hashtag/bech32m?src=hash&amp;ref_src=twsrc%5Etfw">#bech32m</a> and <a href="https://twitter.com/hashtag/Chia?src=hash&amp;ref_src=twsrc%5Etfw">#Chia</a><br><br>1. XCH address is a bech32m encoded of the coin’s puzzle hash.<br>2. NFT Id is a bech32m encoded of the NFT launcher coin id.<br>3. DID is a bech32m encoded of the DID launcher coin id.</p>&mdash; 🌱karlkim.xch🌱 (@kimsk) <a href="https://twitter.com/kimsk/status/1566728274893742083?ref_src=twsrc%5Etfw">September 5, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

https://twitter.com/kimsk/status/1593458381188395008
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">GM <a href="https://twitter.com/hashtag/Chialisper?src=hash&amp;ref_src=twsrc%5Etfw">#Chialisper</a>!<br>When I first learned about <a href="https://twitter.com/hashtag/Chia?src=hash&amp;ref_src=twsrc%5Etfw">#Chia</a> <a href="https://twitter.com/hashtag/DID?src=hash&amp;ref_src=twsrc%5Etfw">#DID</a>, one question arose. How do I verify that a specific person owns a given DID? <br><br>Thanks <a href="https://twitter.com/trepca?ref_src=twsrc%5Etfw">@trepca</a> for quickly answering my question! 💚 <a href="https://t.co/BBLvHk0mQL">pic.twitter.com/BBLvHk0mQL</a></p>&mdash; 🌱karlkim.xch🌱 (@kimsk) <a href="https://twitter.com/kimsk/status/1593458381188395008?ref_src=twsrc%5Etfw">November 18, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

## Notebooks

- [Create DID](./create.ipynb)
- [DID Hint](./hints.ipynb)
- [Get Synthetic PK](./get-synthetic-pk.ipynb)
- [Update Metadata](./update-metadata.ipynb)
- [Transfer DID](./transfer.ipynb)

## References
### Video
- [Introduction to Decentralized Identifiers (DID) - by Ivan Herman (W3C)](https://www.youtube.com/watch?v=t8lMCmjPKq4)
    - [slide](https://iherman.github.io/did-talks/talks/2020-Fintech/#/)

- [What are Decentralized Identifiers (DIDs)?](https://www.youtube.com/watch?v=gWgAgpfLEIQ)
> Similar to email address or phone number as it's globally unique and you can proove that you own one.

> Difference is you entirely control the identifier once it's created
>    - Private Key/Public Key Cryptography
>    - The owner knows the private key
>    - The public key is known to the public

- [Decentralized identity explained](https://www.youtube.com/watch?v=Ew-_F-OtDFI)
> We need digital identifiers that individual can own independently of any entity or organization.

> public key is stored in distributed ledger (i.e., blockchain)

- [Decentralized Identifiers (DIDs) - The Fundamental Building Block of Self Sovereign Identity](youtube.com/watch?v=Jcfy9wd5bZI)
- [Decentralized identifiers (DIDs) fundamentals and deep dive](https://www.youtube.com/watch?v=SHuRRaOBMz4)

### Misc
- [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/)
- [Use Cases and Requirements for Decentralized Identifiers](https://www.w3.org/TR/did-use-cases/)
- [DID Specification Registries](https://www.w3.org/TR/did-spec-registries/)

- [A Primer for Decentralized Identifiers](https://w3c-ccg.github.io/did-primer/)
> a decentralized identifier (DID) is simply a new type of globally unique identifier.

> UUIDs are not globally resolvable and URNs – if resolvable – require a centralized registration authority. In addition, neither UUIDs or URNs inherently address a third characteristic – the ability to cryptographically verify ownership of the identifier.

> DID infrastructure can be thought of as a global key-value database in which the database is all DID-compatible blockchains, distributed ledgers, or decentralized networks.

- [namsdao](https://www.namesdao.org/)

### Chia
- [ChiaLisp & Decentralized Identity](https://www.youtube.com/watch?v=zAG9KeMTZw8)
- [DID RPCs](https://docs.chia.net/docs/12rpcs/did_rpcs)
- [DID CLI Reference](https://docs.chia.net/docs/13cli/did_cli)
- [DIDs](https://chialisp.com/dids)
- [generate_new_decentralised_id](https://github.com/Chia-Network/chia-blockchain/blob/main/chia/wallet/did_wallet/did_wallet.py#L1108)