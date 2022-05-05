from blspy import (AugSchemeMPL, G2Element)

from keys import *
from messages import *

agg_pk = pk1 + pk2 + pk3
print(f"pk1:\t{pk1}")
print(f"pk2:\t{pk2}")
print(f"pk3:\t{pk3}")
print(f"agg_pk:\t{agg_pk}")
print()
print(f"m1:\t{m1}")

sig1: G2Element = AugSchemeMPL.sign(sk1, m1, agg_pk)
sig2: G2Element = AugSchemeMPL.sign(sk2, m1, agg_pk)
sig3: G2Element = AugSchemeMPL.sign(sk3, m1, agg_pk)
agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])
print()
print(f"sig1:\t{sig1}")
print(f"sig2:\t{sig2}")
print(f"sig3:\t{sig3}")
print(f"agg_sig:\t{agg_sig}")
assert AugSchemeMPL.verify(agg_pk, m1, agg_sig)