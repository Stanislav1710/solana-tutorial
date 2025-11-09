from solders.keypair import Keypair


kp = Keypair()
pub = kp.pubkey()

print("Адрес (base58):", str(pub))
print("Публичный ключ, байты:", len(bytes(pub)))
print("Keypair, байты:", len(bytes(kp)))
print("Keypair, hex:", bytes(kp).hex()[:64], "...")
