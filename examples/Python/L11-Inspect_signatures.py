from solders.keypair import Keypair
from solders.message import Message
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client


with open("course_wallet.bin", "rb") as f:
    payer = Keypair.from_bytes(f.read())

client = Client("https://api.devnet.solana.com")
ix = transfer(TransferParams(from_pubkey=payer.pubkey(), to_pubkey=payer.pubkey(), lamports=1))
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], payer.pubkey(), rbh)

tx = Transaction([payer], msg, rbh)
tx.partial_sign([payer], rbh)

raw = bytes(tx)
print("Первые 16 байт:", raw[:16].hex())
print("Длина raw:", len(raw))
