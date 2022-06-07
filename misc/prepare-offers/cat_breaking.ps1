$sw = new-object system.diagnostics.stopwatch
$sw.Start()

$FINGERPRINT = 219821919
$WALLET_ID = 2
$WALLET_ID_JSON = (@{ wallet_id = $WALLET_ID } | ConvertTo-Json)  -replace '"', '\""'
$FEE = 50000000 # 50_000_000 mojos is 0.00005 XCH
$FEE_WALLET_ID_JSON = (@{ wallet_id = 1 } | ConvertTo-Json)  -replace '"', '\""'
$AMOUNT = 1000 # one CAT is 1000 mojos

# set synced wallet
chia wallet show -f $FINGERPRINT | Out-Null
Start-Sleep -s 5

$NUM = 30
$bin_count = [Math]::Ceiling([Math]::Log($NUM) / [Math]::Log(2))

# Phase One
$sw_1 = new-object system.diagnostics.stopwatch
$sw_1.Start()
# 2^n coins
for ($i=1;$i -lt $bin_count;$i++){
    $count = [Math]::Pow(2, $i)
    $amt = [int](($NUM/$count) * $AMOUNT)
    $start = $count - 1
    Write-Host "========="
    Write-Host "$i, $start : $count coins"
    Write-Host "========="
    $addresses =
        chia keys derive -f $FINGERPRINT wallet-address -i $start -n $count
        | % { $_ -replace '(^Wallet address )(.*)(: )', "" }
    
    for($j=0;$j -lt $count;$j++) {
        $idx = $start + $j
        Write-Host "$idx : $amt to $($addresses[$j])" 
    
        $not_enough_spendable = $True
        while($not_enough_spendable){
            $spendable_amount = (chia rpc wallet get_wallet_balance $WALLET_ID_JSON | ConvertFrom-Json).wallet_balance.spendable_balance
            $not_enough_amount =  $spendable_amount -lt $AMOUNT
            $spendable_fee = (chia rpc wallet get_wallet_balance $FEE_WALLET_ID_JSON | ConvertFrom-Json).wallet_balance.spendable_balance
            $not_enough_fee =  $spendable_fee -lt $FEE
            if($not_enough_amount -or $not_enough_fee){
                Start-Sleep -s 5
                Write-Host "spendable_amount: $spendable_amount spendable_fee: $spendable_fee"
            }
            else {
                $not_enough_spendable = $False
            }
        }

        $address = $addresses[$j]
        $cat_spend_json = (@{
            fingerprint = $FINGERPRINT
            wallet_id = $WALLET_ID
            amount = $amt
            fee = $FEE
            inner_address = $address
        } | ConvertTo-Json) -replace '"', '\""'
        # $cat_spend_json
        $result = chia rpc wallet cat_spend $cat_spend_json | ConvertFrom-Json
        Write-Host "txn_id: $($result.transaction_id)"
    }
}
$sw_1.Stop()


# Phase Two
$sw_2 = new-object system.diagnostics.stopwatch
$sw_2.Start()
$FROM_FINGERPRINT = $FINGERPRINT # CAT wallet
$TO_ADDRESS = "txch1qt5p7e5fcnpw9xglt4qtuqkvl5fuy6ddna34vnawyf2xhnzlgf9qfll709" # wallet to create offers
$FROM_WALLET_ID = $WALLET_ID
# $WALLET_ID_JSON = (@{ wallet_id = $FROM_WALLET_ID } | ConvertTo-Json)  -replace '"', '\""'
# $FEE = 50000000 # 50_000_000 mojos is 0.00005 XCH
# $FEE_WALLET_ID_JSON = (@{ wallet_id = 1 } | ConvertTo-Json)  -replace '"', '\""'
# $NUM = 30
# $AMOUNT = 1000 # one CAT is 1000 mojos

# set synced wallet
chia wallet show -f $FROM_FINGERPRINT | Out-Null
Start-Sleep -s 5

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
        Start-Sleep -s 5
        Write-Host "spendable_amount: $spendable_amount spendable_fee: $spendable_fee"
    }

    $cat_spend_json = (@{ 
        fingerprint = $FROM_FINGERPRINT
        wallet_id = $FROM_WALLET_ID
        amount = $AMOUNT
        fee = $FEE
        inner_address = $TO_ADDRESS
    } | ConvertTo-Json) -replace '"', '\""'
    # Write-Host $cat_spend_json
    $result = chia rpc wallet cat_spend $cat_spend_json | ConvertFrom-Json
    Write-Host "txn_id: $($result.transaction_id)"
}


$sw_2.Stop()
$sw.Stop()
Write-Host $sw_1.Elapsed.TotalMinutes
Write-Host $sw_2.Elapsed.TotalMinutes
Write-Host $sw.Elapsed.TotalMinutes