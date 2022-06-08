$keys = @(
    1540817367
    1619840711
    1749937383
    2159580467
    219821919
    2705744614
    668322525
)

$keys
| % { chia keys delete -f $_ }

$wallet_db_path = "$env:CHIA_ROOT/wallet/db"
foreach ($key in $keys) {
    $db_file = "blockchain_wallet_v2_testnet10_$key.sqlite"
    $db_full_path = "$wallet_db_path/$db_file"
    Write-Host "delete $db_full_path"
    if (Test-Path $db_full_path) {
        Write-Host "$db_full_path"
        Remove-Item $db_full_path
    }
}