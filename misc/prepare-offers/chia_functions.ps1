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

# Derive Keys and Decode to Puzzle Hashes
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

function Wait-EnoughSpendable {
    param(
		[Parameter()]
		[int] $WalletId,
        [int64] $Amount
	)
    Write-Host "Wait-EnoughSpendable: $WalletId $Amount " -NoNewline
    $wallet_id_json = (@{ wallet_id = $WalletId } | ConvertTo-Json)  -replace '"', '\""'

    $sw = new-object system.diagnostics.stopwatch
    $sw.Start()
    do {
        Start-Sleep -s 5
        $spendable_amount = (chia rpc wallet get_wallet_balance $wallet_id_json | ConvertFrom-Json).wallet_balance.spendable_balance
        Write-Host "." -NoNewline
    } until ($spendable_amount -ge $Amount) 

    Write-Host ""
    Write-Host "Wait-EnoughSpendable: Spendable: $spendable_amount"
    $sw.Stop()
    Write-Host "Wait-EnoughSpendable: $($sw.Elapsed.TotalMinutes) minutes"
}