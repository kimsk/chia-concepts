from blspy import (AugSchemeMPL, G2Element)

from keys import *
from messages import *

# aggregated public key
agg_pk = pk1 + pk2
sig1: G2Element = AugSchemeMPL.sign(sk1, m1, agg_pk)
sig2: G2Element = AugSchemeMPL.sign(sk2, m1, agg_pk)
agg_sig1 = AugSchemeMPL.aggregate([sig1, sig2])

assert AugSchemeMPL.verify(agg_pk, m1, agg_sig1)

# simple aggregate verify
sig3: G2Element = AugSchemeMPL.sign(sk1, m1)
sig4: G2Element = AugSchemeMPL.sign(sk2, m2)
sig5: G2Element = AugSchemeMPL.sign(sk3, m3)
agg_sig2 = AugSchemeMPL.aggregate([sig3, sig4, sig5])
assert AugSchemeMPL.verify(pk1, m1, sig3)
assert AugSchemeMPL.verify(pk2, m2, sig4)
assert AugSchemeMPL.verify(pk3, m3, sig5)
assert AugSchemeMPL.aggregate_verify(
    [pk1, pk2, pk3],
    [m1, m2, m3],
    agg_sig2)

# aggregate two aggregated signatures
agg_sig = AugSchemeMPL.aggregate([agg_sig2, agg_sig1])

# aggregation order does not matter
assert AugSchemeMPL.aggregate([agg_sig2, agg_sig1]) == AugSchemeMPL.aggregate([agg_sig1, agg_sig2])

assert AugSchemeMPL.aggregate_verify(
    [agg_pk, pk1, pk2, pk3],
    [m1, m1, m2, m3],
    agg_sig)


sig6: G2Element = AugSchemeMPL.sign(sk3, m1)
assert AugSchemeMPL.verify(pk3, m1, sig6)

# aggregate another signature to existing aggregated signature
agg_sig3 = AugSchemeMPL.aggregate([agg_sig, sig6])

# verify individual signatures
assert AugSchemeMPL.verify(agg_pk, m1, agg_sig1)
assert AugSchemeMPL.verify(pk1, m1, sig3)
assert AugSchemeMPL.verify(pk2, m2, sig4)
assert AugSchemeMPL.verify(pk3, m3, sig5)
assert AugSchemeMPL.verify(pk3, m1, sig6)

# aggregate verify
assert AugSchemeMPL.aggregate_verify(
    [agg_pk, pk1, pk2, pk3, pk3],
    [m1, m1, m2, m3, m1],
    agg_sig3)