import time

from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer


client = Client("https://api.devnet.solana.com")

wallet = Keypair()
print("Адрес нового кошелька:", wallet.pubkey())

balance = client.get_balance(wallet.pubkey())
print("Текущий баланс:", balance.value, "lamports")

airdrop = client.request_airdrop(wallet.pubkey(), 1000000000)
print("Airdrop Signature:", airdrop.value)

recipient = Pubkey.from_string("11111111111111111111111111111111")
ix = transfer(TransferParams(from_pubkey=wallet.pubkey(), to_pubkey=recipient, lamports=500000000))
print("Создана инструкция перевода:", ix)


