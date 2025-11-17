from solana.rpc.api import Client
from solders.keypair import Keypair


DEVNET_RPC = "https://api.devnet.solana.com"

LAMPORTS_PER_SOL = 1_000_000_000
AIRDROP_SOL = 1.0

client = Client(DEVNET_RPC)

with open("course_wallet.bin", "rb") as f:
    wallet_bytes = f.read()

wallet = Keypair.from_bytes(wallet_bytes)
pubkey = wallet.pubkey()
print("Адрес course_wallet:", pubkey)

before_resp = client.get_balance(pubkey)
before_lamports = before_resp.value
print("Баланс до airdrop:", before_lamports, "lamports")

amount_lamports = int(AIRDROP_SOL * LAMPORTS_PER_SOL)
airdrop_resp = client.request_airdrop(pubkey, amount_lamports)
sig = airdrop_resp.value
print("Сигнатура airdrop:", sig)

after_resp = client.get_balance(pubkey)
after_lamports = after_resp.value
print("Баланс после airdrop:", after_lamports, "lamports")

print("Баланс в SOL до:", before_lamports / LAMPORTS_PER_SOL)
print("Баланс в SOL после:", after_lamports / LAMPORTS_PER_SOL)