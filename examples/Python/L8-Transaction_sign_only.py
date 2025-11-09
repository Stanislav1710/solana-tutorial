from solders.transaction import Transaction
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.message import Message
from solders.system_program import transfer, TransferParams


client = Client("https://api.devnet.solana.com")
sender = Keypair()
ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=sender.pubkey(), lamports=1))
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], sender.pubkey(), rbh)


tx = Transaction([sender], msg, rbh)
tx.partial_sign([sender], rbh)
print("Размер tx в байтах:", len(bytes(tx)))
print(tx)
