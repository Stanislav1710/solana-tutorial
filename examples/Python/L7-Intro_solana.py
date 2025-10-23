from solana.rpc.api import Client


client = Client("https://api.devnet.solana.com")

print("Подключено:", client.is_connected())
print("Текущий слот:", client.get_slot().value)
print("RPC версия:", client.get_version().value.solana_core)
