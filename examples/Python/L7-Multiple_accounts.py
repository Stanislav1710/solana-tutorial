from solana.rpc.api import Client
from solders.pubkey import Pubkey


client = Client("https://api.devnet.solana.com")

keys = [
    Pubkey.from_string("11111111111111111111111111111111"),
    Pubkey.from_string("SysvarRent111111111111111111111111111111111"),
]

resp = client.get_multiple_accounts(keys)

for i, acc in enumerate(resp.value):
    print(f"Аккаунт {i + 1}:")
    print("  Executable:", acc.executable)
    print("  Owner:", acc.owner)
    print("  Data length:", len(acc.data))
