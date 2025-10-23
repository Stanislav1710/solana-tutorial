from solana.rpc.api import Client
from solders.pubkey import Pubkey


client = Client("https://api.devnet.solana.com")

system_program = Pubkey.from_string("11111111111111111111111111111111")

balance_resp = client.get_balance(system_program)
print("Баланс:", balance_resp.value)

info_resp = client.get_account_info(system_program)
print("Executable:", info_resp.value.executable)
print("Owner:", info_resp.value.owner)
