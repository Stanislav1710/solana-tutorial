from solana.rpc.api import Client, Commitment
from solders.solders import Keypair

client = Client("https://api.devnet.solana.com")

with open("course_wallet.bin", "rb") as f:
    wallet = Keypair.from_bytes(f.read())

pubkey = wallet.pubkey()

slot_processed = client.get_slot(commitment=Commitment("processed")).value
slot_confirmed = client.get_slot(commitment=Commitment("confirmed")).value
slot_finalized = client.get_slot(commitment=Commitment("finalized")).value

print("Слот processed:", slot_processed)
print("Слот confirmed:", slot_confirmed)
print("Слот finalized:", slot_finalized)

b1 = client.get_balance(pubkey, commitment=Commitment("processed")).value
b2 = client.get_balance(pubkey, commitment=Commitment("confirmed")).value
b3 = client.get_balance(pubkey, commitment=Commitment("finalized")).value

print("Баланс (processed):", b1)
print("Баланс (confirmed):", b2)
print("Баланс (finalized):", b3)
