from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.message import Message
from solders.transaction import Transaction


client = Client("https://api.devnet.solana.com")
sender = Keypair()
recipient = Pubkey.from_string("11111111111111111111111111111111")

ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports=1000))
print("Инструкция:", ix)

recent_blockhash = client.get_latest_blockhash().value.blockhash
print("Актуальный блокхеш:", recent_blockhash)

message = Message.new_with_blockhash([ix], sender.pubkey(), recent_blockhash)
print("Сформированное сообщение:", message)

tx = Transaction([sender], message, recent_blockhash)
print("Сформированная транзакция:", tx)

tx.partial_sign([sender], recent_blockhash)

raw = bytes(tx)
print("Tx bytes:", raw)
