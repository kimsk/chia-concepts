# PowerShell object to Json for chia rpc
function Edit-ChiaRpcJson {
    [CmdletBinding()]
    param (
        [Parameter(ValueFromPipeline)]
        [string] $Json
    )
    $Json -replace '"', '\""'
}

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

# Wait until spendable is greater or equal to the amount
function Wait-EnoughSpendable {
    param(
		[Parameter()]
		[int] $WalletId,
        [int64] $Amount
	)
    Write-Host "Wait-EnoughSpendable: $WalletId $Amount " -NoNewline
    $wallet_id_json = 
        @{ wallet_id = $WalletId } 
        | ConvertTo-Json
        | Edit-ChiaRpcJson


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

# Get coins to spend
function Get-Coins {
    param(
		[Parameter()]
		[int] $WalletId,
        [int64] $Amount,
        [int64] $Fee = 0
	)
    $json = @{ 
        wallet_id = $WALLET_ID
        amount = $Amount + $Fee
    }
    | ConvertTo-Json
    | Edit-ChiaRpcJson

    $result = chia rpc wallet select_coins $json 2>&1
    if ($result -like "Request failed:*"){
        # $match = select-string "Request failed: (.*)" -inputobject $result
        # $error_json = $match.Matches.groups[1].value -replace "'", """"
        throw $result
    } else {
        # success
        $result | ConvertFrom-Json
    }
}
