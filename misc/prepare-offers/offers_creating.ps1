$sw = new-object system.diagnostics.stopwatch
$sw.Start()

$OFFER_FINGERPRINT = 2705744614
$OFFER_WALLET_ID = 2
$OFFER_WALLET_ID_JSON = (@{ wallet_id = $OFFER_WALLET_ID } | ConvertTo-Json)  -replace '"', '\""'
$AMOUNT = 1000 # one CAT is 1000 mojos

$FEE_WALLET_ID_JSON = (@{ wallet_id = 1 } | ConvertTo-Json)  -replace '"', '\""'
$FEE = 50000000 # 50_000_000 mojos is 0.00005 XCH

$OFFER_REQUEST_PAYLOAD = "{
    ""offer"": {""2"": -1000, ""1"": 1000000000000},
    ""fee"": $FEE
}" -replace '"', '\""'

$NUM = 60
$OFFER_PATH = "/mnt/e/offers/tdbx"
# set synced wallet
chia wallet show -f $OFFER_FINGERPRINT | Out-Null
Start-Sleep -s 5 

for(($i=0);$i -lt $NUM;$i++)
{
    $not_enough_spendable = $True
    while($not_enough_spendable){
        $spendable_amount = (chia rpc wallet get_wallet_balance $OFFER_WALLET_ID_JSON | ConvertFrom-Json).wallet_balance.spendable_balance
        $enough_amount =  $spendable_amount -ge $AMOUNT
        $spendable_fee = (chia rpc wallet get_wallet_balance $FEE_WALLET_ID_JSON | ConvertFrom-Json).wallet_balance.spendable_balance
        $enough_fee =  $spendable_fee -ge $FEE
        if($enough_amount -and $enough_fee){
        
            $not_enough_spendable = $False
        }

        Start-Sleep -s 5
        Write-Host "spendable_amount: $spendable_amount spendable_fee: $spendable_fee"
    }

    # create offer
    $offer_file_name = "1TDBX_x_1XCH-$i.offer"
    Write-Host $offer_file_name
    $offer = (chia rpc wallet create_offer_for_ids $OFFER_REQUEST_PAYLOAD | ConvertFrom-Json).offer
    $offer | Out-File -FilePath "$OFFER_PATH/$offer_file_name"
}
$sw.Stop()
Write-Host $sw.Elapsed.TotalMinutes