from blspy import (PrivateKey, AugSchemeMPL,
                   G1Element, G2Element)

sk: PrivateKey = PrivateKey.from_bytes(bytes.fromhex("71005b4be2f8a24427dbdcaaae48cab31fa86afc0fe73c40b88b0841f40e4c4d"))
pk: G1Element = sk.get_g1()

message: bytes = bytes("hello chia", 'utf-8')
signature: G2Element = AugSchemeMPL.sign(sk, message)

# Verify the signature
ok: bool = AugSchemeMPL.verify(pk, message, signature)
assert ok
print(signature)