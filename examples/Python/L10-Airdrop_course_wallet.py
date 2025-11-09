from solana.rpc.api import Client
from solders.keypair import Keypair


client = Client("https://api.devnet.solana.com")

with open("course_wallet.bin", "rb") as f:
    kp_bytes = f.read()

kp = Keypair.from_bytes(kp_bytes)

sig = client.request_airdrop(kp.pubkey(), 1_000_000_000)  # 1 SOL = 1e9 lamports
print("Airdrop response:", sig)
