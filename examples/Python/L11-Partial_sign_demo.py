from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import AccountMeta, Instruction
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.transaction import Transaction
from solana.rpc.api import Client


with open("course_wallet.bin", "rb") as f:
    payer = Keypair.from_bytes(f.read())

client = Client("https://api.devnet.solana.com")

co_signer = Keypair()

ix_transfer = transfer(TransferParams(
    from_pubkey=payer.pubkey(),
    to_pubkey=payer.pubkey(),
    lamports=1
))

system_program_id = Pubkey.from_string("11111111111111111111111111111111")
ix_require_cosigner = Instruction(
    program_id=system_program_id,
    accounts=[AccountMeta(pubkey=co_signer.pubkey(), is_signer=True, is_writable=False)],
    data=b""
)

rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix_transfer, ix_require_cosigner], payer.pubkey(), rbh)

tx = Transaction([payer, co_signer], msg, rbh)

tx.partial_sign([payer, co_signer], rbh)

print("OK: транзакция собрана и подписана двумя ключами.")
print("Сериализованный размер:", len(bytes(tx)))
