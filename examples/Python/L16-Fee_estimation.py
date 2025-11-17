from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.transaction import Transaction


DEVNET = "https://api.devnet.solana.com"
client = Client(DEVNET)

with open("course_wallet.bin", "rb") as f:
    kp = Keypair.from_bytes(f.read())

pub = kp.pubkey()
print("Адрес:", pub)

ix = transfer(TransferParams(
    from_pubkey=pub,
    to_pubkey=pub,
    lamports=1
))

latest = client.get_latest_blockhash().value
blockhash = latest.blockhash

msg = Message.new_with_blockhash([ix], pub, blockhash)

fee = client.get_fee_for_message(msg).value
print("Оценка комиссии:", fee, "lamports")

tx = Transaction([kp], msg, blockhash)
tx.partial_sign([kp], blockhash)

sig = client.send_transaction(tx).value
print("Сигнатура:", sig)

st = client.get_signature_statuses([sig]).value[0]
print("Результат:", st)
