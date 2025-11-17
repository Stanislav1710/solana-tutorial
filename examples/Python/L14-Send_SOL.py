from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.transaction import Transaction


DEVNET = "https://api.devnet.solana.com"
client = Client(DEVNET)

with open("course_wallet.bin", "rb") as f:
    wallet = Keypair.from_bytes(f.read())

pubkey = wallet.pubkey()
print("Адрес:", pubkey)

before = client.get_balance(pubkey).value
print("Баланс до:", before, "lamports")

ix = transfer(TransferParams(
    from_pubkey=pubkey,
    to_pubkey=pubkey,
    lamports=1
))

latest = client.get_latest_blockhash().value
blockhash = latest.blockhash

msg = Message.new_with_blockhash([ix], pubkey, blockhash)

tx = Transaction([wallet], msg, blockhash)
tx.partial_sign([wallet], blockhash)

resp = client.send_transaction(tx)
sig = resp.value
print("Сигнатура транзакции:", sig)

status = client.get_signature_statuses([sig]).value[0]
print("Статус выполнения:", status)

after = client.get_balance(pubkey).value
print("Баланс после:", after, "lamports")
