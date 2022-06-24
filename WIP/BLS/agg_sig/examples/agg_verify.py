from blspy import (AugSchemeMPL, G2Element)

from keys import *
from messages import *

print(f"pk1:\t{pk1}")
print(f"pk2:\t{pk2}")
print(f"pk3:\t{pk3}")
print()
print(f"m1:\t{m1}")
print(f"m2:\t{m2}")
print(f"m3:\t{m3}")

sig1: G2Element = AugSchemeMPL.sign(sk1, m1)
sig2: G2Element = AugSchemeMPL.sign(sk2, m2)
sig3: G2Element = AugSchemeMPL.sign(sk3, m3)
agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])
print()
print(f"sig1:\t{sig1}")
print(f"sig2:\t{sig2}")
print(f"sig3:\t{sig3}")
print(f"agg_sig:\t{agg_sig}")
assert AugSchemeMPL.verify(pk1, m1, sig1)
assert AugSchemeMPL.verify(pk2, m2, sig2)
assert AugSchemeMPL.verify(pk3, m3, sig3)
assert AugSchemeMPL.aggregate_verify(
    [pk1, pk2, pk3],
    [m1, m2, m3],
    agg_sig)