$FINGERPRINT = 990489918
$FEE = 500000000 # 500_000_000 mojos is 0.0005 XCH

$WALLET_ID = 1
$NUM = 100
$AMOUNT = $FEE 

$addresses = 
    chia keys derive -f $FINGERPRINT wallet-address -n $NUM 
    | % { $_ -replace '(^Wallet address )(.*)(: )', "" }

$additions = @()
foreach($addr in $addresses) {
    $puzzle_hash = cdv decode $addr
    Write-Host $addr $puzzle_hash
    $addition = @{
        amount = $AMOUNT
        puzzle_hash = $puzzle_hash
    }
    $additions += $addition
}

$select_coins_json = 
    @{ 
        wallet_id = $WALLET_ID
        amount = $AMOUNT * $NUM
    } | ConvertTo-Json

$_select_coins_json = $select_coins_json -replace '"', '\""'
$coins = (chia rpc wallet select_coins $_select_coins_json | ConvertFrom-Json).coins

$json = @{
    wallet_id = 1
    additions = $additions
    fee = 50000000 * $NUM # 0.00005
    coins = $coins
} | ConvertTo-Json
$_json = $json -replace '"', '\""'

$signed_tx = (chia rpc wallet create_signed_transaction $_json | ConvertFrom-Json).signed_tx
$signed_tx_json = $signed_tx | ConvertTo-Json -Depth 4
$_signed_tx_json = $signed_tx_json -replace '"', '\""'
chia rpc wallet send_transaction_multi $_signed_tx_json