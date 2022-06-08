$FINGERPRINT = 2598237524
$NUM = 5
chia keys derive -f $FINGERPRINT wallet-address -n $NUM 
    | % { $_ -replace '(^Wallet address )(.*)(: )', "" }
    | % { cdv decode $_ }