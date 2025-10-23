from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey


client = Client("http://127.0.0.1:8899")

wallet = Keypair()
print("Адрес нового кошелька:", wallet.pubkey())

status = client.is_connected()
print("Подключение активно:", status)

slot = client.get_slot().value
print("Текущий слот:", slot)

address = Pubkey.from_string("11111111111111111111111111111111")
info = client.get_account_info(address)
print("Информация об аккаунте:", info.value)
