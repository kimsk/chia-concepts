from blspy import (AugSchemeMPL, G1Element, G2Element, PrivateKey)

from keys import *
from messages import *

# aggregated public keys
agg_pk: G1Element = pk1 + pk2

# aggregated private keys
agg_sk = PrivateKey.aggregate([sk2, sk1])

print(f'agg_pk:\t\t\t{agg_pk}')
print(f'agg_sk.get_g1():\t{agg_sk.get_g1()}')

# aggregated public keys is the same as the pk of the aggregated private keys
assert agg_sk.get_g1() == agg_pk

sig: G2Element = AugSchemeMPL.sign(agg_sk, m1)
assert AugSchemeMPL.verify(agg_pk, m1, sig)
