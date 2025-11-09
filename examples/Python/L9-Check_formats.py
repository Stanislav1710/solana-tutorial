from solders.keypair import Keypair
from solders.pubkey import Pubkey


kp = Keypair()
pub = kp.pubkey()

print("Адрес (base58):", str(pub))
print("Pubkey hex:", bytes(pub).hex())

restored = Pubkey.from_string(str(pub))
print("Совпадает:", restored == pub)
