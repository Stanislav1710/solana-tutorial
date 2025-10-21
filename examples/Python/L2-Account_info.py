from solana.rpc.api import Client
from solders.pubkey import Pubkey

client = Client("https://api.devnet.solana.com")
address = Pubkey.from_string("11111111111111111111111111111111")  # пример: системная программа
info = client.get_account_info(address)
print(info)
print(bytes(info.value.data).decode())
