- [DAOInfo](https://github.com/Chia-Network/chia-blockchain/blob/2429cd79e775ad9bc6721e7153f0103ffbe70e79/chia/wallet/dao_wallet/dao_info.py#L23)

- [ProposalInfo](https://github.com/Chia-Network/chia-blockchain/blob/2429cd79e775ad9bc6721e7153f0103ffbe70e79/chia/wallet/dao_wallet/dao_info.py#L15)



## Files
### Puzzles
```sh
❯ gci -Recurse -Filter "*dao*" |
∙ % { $_.FullName -replace $PWD,"" } |
∙ ? { $_ -like "*puzzles*" -and `
∙ $_ -notlike "*__pycache__*" -and $_ -notlike "/build*" -and $_ -notlike "*.hex*" }
/chia/wallet/dao_wallet/dao_wallet_puzzles.py
*/chia/wallet/puzzles/dao_cat_buy_in.clvm
/chia/wallet/puzzles/dao_dividend_timer.clvm
/chia/wallet/puzzles/dao_dividend.clvm
*/chia/wallet/puzzles/dao_finished_state.clvm
*/chia/wallet/puzzles/dao_lockup.clvm
*/chia/wallet/puzzles/dao_proposal_timer.clvm
*/chia/wallet/puzzles/dao_proposal.clvm
/chia/wallet/puzzles/dao_resale_prevention_layer.clvm
*/chia/wallet/puzzles/dao_spend_proposal.clvm
*/chia/wallet/puzzles/dao_treasury.clvm
*/chia/wallet/puzzles/dao_update_proposal.clvm
*/chia/wallet/puzzles/genesis_by_coin_id_or_proposal.clvm

```

### Tests
```sh
❯ gci -Recurse -Filter "*dao*" |
∙ % { $_.FullName -replace $PWD,"" } |
∙ ? { $_ -like "*tests*" -and $_ -notlike "*__pycache__*" }
/tests/wallet/cat_wallet/test_dao_cat_wallet.py
/tests/wallet/cat_wallet/test_dao_clvm.py
/tests/wallet/cat_wallet/test_dao_spendbundles.py
/tests/wallet/cat_wallet/test_dao_wallets.py
```


## DAO Creation
https://github.com/Chia-Network/chia-blockchain/blob/539f0921a41804b6237670e723fc112b0510acbd/chia/wallet/dao_wallet/dao_wallet.py#L86

### create_new_dao_and_wallet (`amount_of_cats: uint64`)
#### [generate_new_dao](https://github.com/Chia-Network/chia-blockchain/blob/539f0921a41804b6237670e723fc112b0510acbd/chia/wallet/dao_wallet/dao_wallet.py#L561)

- "treasury_id": launcher_coin.name()
```
    amount_of_cats: uint64,
    attendance_required_percentage: uint64,
    proposal_pass_percentage: uint64,  # reminder that this is between 0 - 10,000
    proposal_timelock: uint64,
```
```
    launcher_coin = Coin(origin.name(), genesis_launcher_puz.get_tree_hash(), 1)
    cat_tail_info = {
        "identifier": "genesis_by_id_or_proposal",
        "treasury_id": launcher_coin.name(),
        "coins": different_coins,
    }
```

https://github.com/Chia-Network/chia-blockchain/blob/539f0921a41804b6237670e723fc112b0510acbd/chia/wallet/dao_wallet/dao_wallet.py#L599
https://github.com/Chia-Network/chia-blockchain/blob/f1c15b2e3bd0b7f90366d715421e7282b07d7fbf/chia/wallet/dao_wallet/dao_utils.py#L253
```
# launcher_coin.name() is treasury_id
cat_tail = generate_cat_tail(cat_origin.name(), launcher_coin.name())
```

##### [DAOCATWallet.create_new_cat_wallet](https://github.com/Chia-Network/chia-blockchain/blob/539f0921a41804b6237670e723fc112b0510acbd/chia/wallet/dao_wallet/dao_wallet.py#L623)
- CAT (with genesis_by_id_or_proposal) is created
- This will also mint the coins
https://github.com/Chia-Network/chia-blockchain/blob/a7883b573ff35abb265860e98e8695b1281d927e/chia/wallet/cat_wallet/cat_wallet.py#L153
```
cat_tail_info,
amount_of_cats,
```

##### [create treasury](https://github.com/Chia-Network/chia-blockchain/blob/539f0921a41804b6237670e723fc112b0510acbd/chia/wallet/dao_wallet/dao_wallet.py#L646)
```
dao_treasury_puzzle = get_treasury_puzzle(
    launcher_coin.name(),
    cat_tail.get_tree_hash(),
    amount_of_cats,
    attendance_required_percentage,
    proposal_pass_percentage,
    proposal_timelock,
)
```        

- [DAOInfo now has `cat_wallet_id` and `treasury_id`](https://github.com/Chia-Network/chia-blockchain/blob/021baba6c9e81e050742dc17c91b38c36329cea8/tests/wallet/cat_wallet/test_dao_wallets.py#L77)
```
DAOInfo(treasury_id=<bytes32: a14daf55d41ced6419bcd011fbc1f74ab9567fe55340d88435aa6493d628fa47>, cat_wallet_id=3, proposals_list=[], parent_info=[], current_treasury_coin=None, current_treasury_innerpuz=None)
```

https://github.com/Chia-Network/chia-blockchain/blob/bb1e3aed746dd9b65606cdaf674a37e20f8f667f/chia/wallet/puzzles/genesis_by_coin_id_or_proposal.clvm#L8




Test CAT Spend
https://github.com/Chia-Network/chia-blockchain/blob/42b2b995679616da9f18a08a6cc7871f4bc06e20/tests/wallet/cat_wallet/test_dao_cat_wallet.py#L55

CATWallet.create_new_cat_wallet(
https://github.com/Chia-Network/chia-blockchain/blob/42b2b995679616da9f18a08a6cc7871f4bc06e20/tests/wallet/cat_wallet/test_dao_cat_wallet.py#L89