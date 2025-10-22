from solana.rpc.api import Client
from solders.pubkey import Pubkey


client = Client("https://api.devnet.solana.com")

address = Pubkey.from_string("11111111111111111111111111111111")

balance = client.get_balance(address)
print("Баланс:", balance.value, "lamports")

block_height = client.get_block_height()
print("Высота текущего блока:", block_height.value)
