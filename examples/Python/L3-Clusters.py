from solana.rpc.api import Client
from solders.pubkey import Pubkey


address = Pubkey.from_string("11111111111111111111111111111111")

client_dev = Client("https://api.devnet.solana.com")
client_test = Client("https://api.testnet.solana.com")
client_main = Client("https://api.mainnet-beta.solana.com")

slot_dev = client_dev.get_slot().value
slot_test = client_test.get_slot().value
slot_main = client_main.get_slot().value

print(f"Devnet slot: {slot_dev}")
print(f"Testnet slot: {slot_test}")
print(f"Mainnet slot: {slot_main}")

balance_dev = client_dev.get_balance(address).value
balance_test = client_test.get_balance(address).value
balance_main = client_main.get_balance(address).value

print(f"Devnet balance: {balance_dev} lamports")
print(f"Testnet balance: {balance_test} lamports")
print(f"Mainnet balance: {balance_main} lamports")
