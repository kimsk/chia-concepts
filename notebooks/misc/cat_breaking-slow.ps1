$sw = new-object system.diagnostics.stopwatch
$sw.Start()

$FROM_FINGERPRINT = 2952324759
$TO_ADDRESS = "txch1fusur439750ps3064m98n4kakv4rezvq2mqjnruu44kp5n8ng8ssgqgg2p"
$FROM_WALLET_ID = 2
$WALLET_ID_JSON = (@{ wallet_id = $FROM_WALLET_ID } | ConvertTo-Json)  -replace '"', '\""'
$FEE = 500000000 # 500000000 mojos is 0.0005 XCH
$FEE_WALLET_ID_JSON = (@{ wallet_id = 1 } | ConvertTo-Json)  -replace '"', '\""'
$NUM = 90
$AMOUNT = 1000 # one CAT is 1000 mojos

# set synced wallet
chia wallet show -f $FROM_FINGERPRINT | Out-Null
Start-Sleep -s 10

# break coin
for(($i=0);$i -lt $NUM;$i++)
{
    $not_enough_spendable = $True
    while($not_enough_spendable){
        $spendable_amount = (chia rpc wallet get_wallet_balance $WALLET_ID_JSON | ConvertFrom-Json).wallet_balance.spendable_balance
        $enough_amount =  $spendable_amount -ge $AMOUNT
        $spendable_fee = (chia rpc wallet get_wallet_balance $FEE_WALLET_ID_JSON | ConvertFrom-Json).wallet_balance.spendable_balance
        $enough_fee =  $spendable_fee -ge $FEE
        if($enough_amount -and $enough_fee){
            $not_enough_spendable = $False
        }
        Start-Sleep -s 10
        Write-Host "spendable_amount: $spendable_amount spendable_fee: $spendable_fee"
    }

    $cat_spend_json = (@{ 
        fingerprint = $FROM_FINGERPRINT
        wallet_id = $FROM_WALLET_ID
        amount = $AMOUNT
        fee = $FEE
        inner_address = $TO_ADDRESS
    } | ConvertTo-Json) -replace '"', '\""'
    $result = chia rpc wallet cat_spend $cat_spend_json | ConvertFrom-Json
    Write-Host "txn_id: $($result.transaction_id)"
}

$sw.Stop()
Write-Host $sw.Elapsed.TotalMinutes

# $select_coins_json = (@{ wallet_id = $WALLET_ID; amount = $AMOUNT } | ConvertTo-Json) -replace '"', '\""'
#     $coins = chia rpc wallet select_coins $select_coins_json | jq
#     Write-Host $coins

