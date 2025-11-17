from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.instruction import Instruction, AccountMeta
from solders.message import Message
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams


DEVNET = "https://api.devnet.solana.com"
client = Client(DEVNET)

with open("course_wallet.bin", "rb") as f:
    main = Keypair.from_bytes(f.read())

main_pub = main.pubkey()
print("Основной адрес:", main_pub)

A = Keypair()
B = Keypair()

print("Доп. подписант A:", A.pubkey())
print("Доп. подписант B:", B.pubkey())

base_ix = transfer(TransferParams(
    from_pubkey=main_pub,
    to_pubkey=main_pub,
    lamports=1
))

accounts = list(base_ix.accounts)
accounts.append(AccountMeta(pubkey=A.pubkey(), is_signer=True, is_writable=False))
accounts.append(AccountMeta(pubkey=B.pubkey(), is_signer=True, is_writable=False))

ix = Instruction(
    program_id=base_ix.program_id,
    accounts=accounts,
    data=base_ix.data
)

latest = client.get_latest_blockhash().value
blockhash = latest.blockhash

msg = Message.new_with_blockhash([ix], main_pub, blockhash)

tx = Transaction.new_unsigned(msg)

tx.partial_sign([main], blockhash)

tx.partial_sign([A], blockhash)
tx.partial_sign([B], blockhash)

sig = client.send_transaction(tx).value
print("Сигнатура:", sig)

status = client.get_signature_statuses([sig]).value[0]
print("Статус:", status)
