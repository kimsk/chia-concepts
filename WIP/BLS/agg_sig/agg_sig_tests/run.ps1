$spend_bundle = python ./both_agg_sig.py 
    | Tee-Object -Variable spend_bundle_json
    | ConvertFrom-Json
$puzzle = opd ($spend_bundle.coin_spends[0].puzzle_reveal).SubString(2)
$solution = opd ($spend_bundle.coin_spends[0].solution).SubString(2)
brun $puzzle $solution