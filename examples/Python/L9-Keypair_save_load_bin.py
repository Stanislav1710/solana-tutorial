from solders.keypair import Keypair


kp = Keypair()
with open("wallet.bin", "wb") as f:
    f.write(bytes(kp))

with open("wallet.bin", "rb") as f:
    raw = f.read()
kp2 = Keypair.from_bytes(raw)

print("Совпадает:", kp.pubkey() == kp2.pubkey())
