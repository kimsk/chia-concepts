from blspy import (PrivateKey, AugSchemeMPL,
                   G1Element, G2Element)

sk1: PrivateKey = PrivateKey.from_bytes(bytes.fromhex("0a900677882bcfa970724a381900e7b6c0d40425fda8a2d1f2db90a13d960472"))
pk1: G1Element = sk1.get_g1()
assert pk1 == G1Element.from_bytes(bytes.fromhex("a4d7da9a1c5210352e4487abc45cc09ca7e523630740e208087c4eb5f0c7ea85819c7affae1b1c846feabf49b071ad1d"))
sk2: PrivateKey = PrivateKey.from_bytes(bytes.fromhex("0f90b1a9ca144b969283a989eb8c5273cbe192df58eb79e551ed538759f9ee14"))
pk2: G1Element = sk2.get_g1()
assert pk2 == G1Element.from_bytes(bytes.fromhex("a4a0b8aed35ad944b287d0a46245c0bc66e1b0ae21cfa0190d90f2dc0a16b0482c44ad5f8b7256357d4f108d4ed5a9d1"))
sk3: PrivateKey = PrivateKey.from_bytes(bytes.fromhex("12acd472632e04bf69ff6bf9715e37fdd8d752874e29ae44ba8d53bb3744b4fc"))
pk3: G1Element = sk3.get_g1()
assert pk3 == G1Element.from_bytes(bytes.fromhex(" a4d62928c171673d15f268812499870346e7ce2d78321a23fc9584ea3c21f090a84215cc522a15de967a96aaae710587"))

# a message is signed with three different private keys to get three signatures
message = "hello chia"
message_as_bytes = bytes(message, "utf-8")

# aggregate three public keys to one aggregated public key
agg_pk = pk1 + pk2 + pk3
sig1: G2Element = AugSchemeMPL.sign(sk1, message_as_bytes, agg_pk)
sig2: G2Element = AugSchemeMPL.sign(sk2, message_as_bytes, agg_pk)
sig3: G2Element = AugSchemeMPL.sign(sk3, message_as_bytes, agg_pk)

# aggregate three signatures to one and verify with aggregated public keys
agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])
assert AugSchemeMPL.verify(agg_pk, message_as_bytes, agg_sig)
assert AugSchemeMPL.aggregate_verify([agg_pk], [message_as_bytes], agg_sig)

# aggregate sign without aggregated public keys
sig1: G2Element = AugSchemeMPL.sign(sk1, message_as_bytes)
sig2: G2Element = AugSchemeMPL.sign(sk2, message_as_bytes)
sig3: G2Element = AugSchemeMPL.sign(sk3, message_as_bytes)
agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])
assert AugSchemeMPL.aggregate_verify(
    [pk1, pk2, pk3],
    [message_as_bytes, message_as_bytes, message_as_bytes],
    agg_sig)

# verify signatures
assert AugSchemeMPL.verify(pk1, message_as_bytes, sig1)
assert AugSchemeMPL.verify(pk2, message_as_bytes, sig2)
assert AugSchemeMPL.verify(pk3, message_as_bytes, sig3)



# a key with three messages
m1 = bytes("1", "utf-8")
m2 = bytes("2", "utf-8")
m3 = bytes("3", "utf-8")

sig1: G2Element = AugSchemeMPL.sign(sk1, m1)
sig2: G2Element = AugSchemeMPL.sign(sk1, m2)
sig3: G2Element = AugSchemeMPL.sign(sk1, m3)

assert AugSchemeMPL.verify(pk1, m1, sig1)
assert AugSchemeMPL.verify(pk1, m2, sig2)
assert AugSchemeMPL.verify(pk1, m3, sig3)

# aggregate verify
agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])
assert AugSchemeMPL.aggregate_verify([pk1, pk1, pk1], [m1, m2, m3], agg_sig)


# 3 keys, 3 messages, aggregated
m1 = bytes("1", "utf-8")
m2 = bytes("2", "utf-8")
m3 = bytes("3", "utf-8")

sig1: G2Element = AugSchemeMPL.sign(sk1, m1)
sig2: G2Element = AugSchemeMPL.sign(sk2, m2)
sig3: G2Element = AugSchemeMPL.sign(sk3, m3)

assert AugSchemeMPL.verify(pk1, m1, sig1)
assert AugSchemeMPL.verify(pk2, m2, sig2)
assert AugSchemeMPL.verify(pk3, m3, sig3)

# aggregate verify
agg_sig = AugSchemeMPL.aggregate([sig1, sig2, sig3])
assert AugSchemeMPL.aggregate_verify([pk1, pk2, pk3], [m1, m2, m3], agg_sig)

# https://github.com/Chia-Network/bls-signatures/blob/0dfd8b6415670608d60523fb4de3022d8c676096/python-bindings/test.py#L43