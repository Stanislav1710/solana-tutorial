from solders.keypair import Keypair


with open("course_wallet.bin", "rb") as f:
    raw = f.read()

kp = Keypair.from_bytes(raw)
print("Загружен pubkey:", kp.pubkey())
