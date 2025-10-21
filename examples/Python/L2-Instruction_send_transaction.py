from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message
from solana.rpc.api import Client

client = Client("https://api.devnet.solana.com")

sender_kp = Keypair()
recipient = Pubkey.from_string("11111111111111111111111111111111")

ix = transfer(
    TransferParams(
        from_pubkey=sender_kp.pubkey(),
        to_pubkey=recipient,
        lamports=1000
    )
)

recent_blockhash = client.get_latest_blockhash().value.blockhash

message = Message.new_with_blockhash(
    [ix],
    sender_kp.pubkey(),
    recent_blockhash
)

tx = Transaction([sender_kp], message, recent_blockhash)
tx.partial_sign([sender_kp], recent_blockhash)
resp = client.send_transaction(tx)  # client.simulate_transaction(tx)
print(resp)


# print(simulation)
