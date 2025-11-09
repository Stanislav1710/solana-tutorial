from solders.message import Message
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client


client = Client("https://api.devnet.solana.com")
sender = Keypair()
recipient = sender.pubkey()
ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports=1))
recent_blockhash = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], sender.pubkey(), recent_blockhash)
print(msg)
