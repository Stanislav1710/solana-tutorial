from solana.rpc.api import Client


client = Client("https://api.devnet.solana.com")

latest = client.get_latest_blockhash().value
print("blockhash:", latest.blockhash)
print("last_valid_block_height:", latest.last_valid_block_height)
