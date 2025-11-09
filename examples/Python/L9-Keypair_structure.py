from solders.keypair import Keypair


kp = Keypair()
print("Seed (32 байта):", len(kp.secret()))
print("Pubkey (32 байта):", len(bytes(kp.pubkey())))
print("Сериализованный (64 байта):", len(bytes(kp)))
