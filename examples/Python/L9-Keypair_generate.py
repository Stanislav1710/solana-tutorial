from solders.keypair import Keypair


kp = Keypair()
print("Адрес (pubkey):", kp.pubkey())
print("Длина bytes(kp):", len(bytes(kp)))
