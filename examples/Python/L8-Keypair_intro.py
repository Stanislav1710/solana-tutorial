from solders.keypair import Keypair

kp = Keypair()
print("Адрес:", kp.pubkey())
print("Секрет+паблик (64 байта):", len(bytes(kp)))
