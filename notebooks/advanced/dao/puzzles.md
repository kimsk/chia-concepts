## /chia/wallet/puzzles/dao_treasury.clvm
> This represents the controls over the money that the treasury owns. Money can be sent to this via p2_singleton or by spending this coin through the "add money" spend case

## /chia/wallet/puzzles/genesis_by_coin_id_or_proposal.clvm
> This checker allows new CATs to be created from an initial mint with a particular coin id as parent OR the checker also allows new CATS to be created from a passed proposal with the correct TREASURY_ID The DAO_TREASURY_ID is curried in, making this lineage_check program unique and giving the CAT it's unique affiliation with the DAO

## /chia/wallet/puzzles/dao_proposal.clvm
> This is a proposal which lives inside a singleton, it represents a proposed way to spend DAO money. If the proposal passes the INNERPUZ inside it will run, and the DAO Treasury will accept a spend to change itself or spend money

## /chia/wallet/puzzles/dao_update_proposal.clvm
> This puzzle is a generic inner puzzle for a DAO proposal and works with either XCH or CAT minting. It curries in a list of conditions which are produced if the proposal runs its "pass" spend.

## /chia/wallet/puzzles/dao_spend_proposal.clvm
> This puzzle is a generic inner puzzle for a DAO proposal and works with either XCH or CAT minting. It curries in a list of conditions which are produced if the proposal runs its "pass" spend.

## /chia/wallet/puzzles/dao_lockup.clvm
> This code is the "voting mode" for a DAO CAT. The coin can be spent from this state to vote on a proposal or claim a dividend. It locks the CAT in while it has active votes/dividends going on. Once a vote or dividend closes, then the coin can spend itself to remove that coin from the "active list". If the "active list" is empty the coin can leave the voting mode

## /chia/wallet/puzzles/dao_finished_state.clvm
> It is an oracle which simply recreates itself and emits an announcement that it has concluded operation

## /chia/wallet/puzzles/dao_cat_buy_in.clvm
> This is an innerpuz inside a DAO CAT, or any CAT, or even any coin, which locks it up until a payment gets made

## /chia/wallet/puzzles/dao_proposal_timer.clvm
> This is a persistent timer for a proposal which allows it to have a relative time that survives despite it being recreated. It has a curried TIMELOCK, which is applied as a ASSERT_HEIGHT_RELATIVE. It creates/asserts announcements to pair it with the finishing spend of a proposal.

## /chia/wallet/puzzles/dao_resale_prevention_layer.clvm
> The function of this file is to force the DAO CAT underneath it to stay in locked voting mode for TIMELOCK period of time.