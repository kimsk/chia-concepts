# Verify that wallet with the $FINGERPRINT is synced
function Wait-For-Synced-Wallet {
    param(
        [Parameter()]
        [Int64] $fingerprint
    )
    $sw = new-object system.diagnostics.stopwatch
    $sw.Start()
    Write-Host "Wait-For-Synced-Wallet: $fingerprint " -NoNewline

    chia wallet show -f $FINGERPRINT | Out-Null

    do {
        Start-Sleep -s 5
        $sync_status = chia rpc wallet get_sync_status | ConvertFrom-Json
        Write-Host "." -NoNewline
    } until ($sync_status.synced) 

    $sw.Stop()
    Write-Host ""
    Write-Host "Wait-For-Synced-Wallet: $($sw.Elapsed.TotalMinutes) minutes"
}

$sw = new-object system.diagnostics.stopwatch
$sw.Start()

$FINGERPRINT = 4108344430 # fingerprint of your wallet
Wait-For-Synced-Wallet -fingerprint $FINGERPRINT

$FEE = 50000000 # 50_000_000 mojos is 0.00005 XCH

$WALLET_ID = 1
$NUM = 200 # Prepare 200 0.00005 XCH coins
$AMOUNT = $FEE

$addresses = 
    chia keys derive -f $FINGERPRINT wallet-address -n $NUM 
    | % { $_ -replace '(^Wallet address )(.*)(: )', "" }

$additions = @()
foreach($addr in $addresses) {
    $puzzle_hash = cdv decode $addr
    $addition = @{
        amount = $AMOUNT
        puzzle_hash = $puzzle_hash
    }
    $additions += $addition
}

$txn_fee = $FEE * $NUM # fee for send_transaction_multi transaction
$select_coins_json = 
    @{ 
        wallet_id = $WALLET_ID
        amount = ($AMOUNT * $NUM) + $txn_fee
    } | ConvertTo-Json

$_select_coins_json = $select_coins_json -replace '"', '\""'
$coins = (chia rpc wallet select_coins $_select_coins_json | ConvertFrom-Json).coins

$json = @{
    wallet_id = 1
    additions = $additions
    fee = $txn_fee
    coins = $coins
} | ConvertTo-Json
$_json = $json -replace '"', '\""'

$signed_tx = (chia rpc wallet create_signed_transaction $_json | ConvertFrom-Json).signed_tx
$signed_tx_json = $signed_tx | ConvertTo-Json -Depth 4
$_signed_tx_json = $signed_tx_json -replace '"', '\""'
chia rpc wallet send_transaction_multi $_signed_tx_json

$sw.Stop()
Write-Host $sw.Elapsed.TotalMinutes