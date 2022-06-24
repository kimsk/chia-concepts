while($True){
    # only get 10 offers max for each call
    $offers = (chia rpc wallet get_all_offers | ConvertFrom-Json).trade_records
    if ($offers.Length -le 0) {
        break
    }

    foreach ($offer in $offers) {
        $payload = @{
            trade_id = $offer.trade_id
            secure = $False
        } 
        | ConvertTo-Json
        | % { $_ -replace '"', '\""'}
        Write-Host $offer.trade_id
        chia rpc wallet cancel_offer $payload | Out-Null
    }
}