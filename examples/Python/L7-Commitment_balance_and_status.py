from solana.rpc.api import Client, Commitment
from solders.pubkey import Pubkey


client = Client("https://api.devnet.solana.com")
address = Pubkey.from_string("11111111111111111111111111111111")

b_fast = client.get_balance(address, commitment=Commitment("processed")).value
b_safe = client.get_balance(address, commitment=Commitment("finalized")).value
print("Баланс (processed):", b_fast)
print("Баланс (finalized):", b_safe)
