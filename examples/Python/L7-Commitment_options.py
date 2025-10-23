from solana.rpc.api import Client, Commitment


client = Client("https://api.devnet.solana.com")

slot_finalized = client.get_slot(commitment=Commitment("finalized")).value
print("Слот (finalized):", slot_finalized)

slot_processed = client.get_slot(commitment=Commitment("processed")).value
print("Слот (processed):", slot_processed)
