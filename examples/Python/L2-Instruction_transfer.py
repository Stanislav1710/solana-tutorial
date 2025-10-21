from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer


sender = Keypair()
recipient = Pubkey.from_string("11111111111111111111111111111111")

ix = transfer(
    TransferParams(
        from_pubkey=sender.pubkey(),
        to_pubkey=recipient,
        lamports=1000
    )
)

print(ix)

