# Verify that wallet with the $FINGERPRINT is synced
function Wait-SyncedWallet {
    param(
        [Parameter()]
        [Int64] $fingerprint
    )
    $sw = new-object system.diagnostics.stopwatch
    $sw.Start()
    Write-Host "Wait-SyncedWallet: $fingerprint " -NoNewline

    chia wallet show -f $FINGERPRINT | Out-Null

    do {
        Start-Sleep -s 5
        $sync_status = chia rpc wallet get_sync_status | ConvertFrom-Json
        Write-Host "." -NoNewline
    } until ($sync_status.synced) 

    $sw.Stop()
    Write-Host ""
    Write-Host "Wait-SyncedWallet: $($sw.Elapsed.TotalMinutes) minutes"
}

function Get-DerivedPuzzleHashes {
    param(
        [Parameter()]
        [Int64] $fingerprint,
        [Int] $num
    )
    $sw = new-object system.diagnostics.stopwatch
    $sw.Start()
    Write-Host "Get-DerivedPuzzleHashes: $fingerprint $num " -NoNewline

    $puzzle_hashes = 
        chia keys derive -f $fingerprint wallet-address -n $num 
        | ForEach-Object { $_ -replace '(^Wallet address )(.*)(: )', "" }
        | ForEach-Object { Write-Host "." -NoNewline; cdv decode $_ }

    $sw.Stop()
    Write-Host "Get-DerivedPuzzleHashes: $($sw.Elapsed.TotalMinutes) minutes"
    $result = $puzzle_hashes
    return $result
}

$sw = new-object system.diagnostics.stopwatch
$sw.Start()

$FINGERPRINT = 4108344430 # fingerprint of your wallet
Wait-SyncedWallet -fingerprint $FINGERPRINT

$FEE = 50000000 # 50_000_000 mojos is 0.00005 XCH

$WALLET_ID = 1
$NUM = 200 # Prepare 200 0.00005 XCH coins
$AMOUNT = $FEE

$puzzle_hashes = Get-DerivedPuzzleHashes -fingerprint $FINGERPRINT -num $NUM

$additions = @()
foreach($puzzle_hash in $puzzle_hashes) {
    
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
Write-Host "XCH Breaking: $($sw.Elapsed.TotalMinutes)"