from solders.keypair import Keypair


kp = Keypair()
print("Публичный ключ:", kp.pubkey())
print("Приватный ключ (bytes):", kp.secret())
