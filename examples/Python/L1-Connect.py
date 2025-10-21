from solana.rpc.api import Client


client = Client("https://api.devnet.solana.com")
version = client.get_version().value.solana_core
print("Devnet node version:", version)
