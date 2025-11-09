from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import CreateAccountParams, create_account


payer = Keypair()
new_account = Keypair()
program_owner = Pubkey.from_string("11111111111111111111111111111111")

ix = create_account(CreateAccountParams(
    from_pubkey=payer.pubkey(),
    to_pubkey=new_account.pubkey(),
    lamports=1000000,
    space=64,
    owner=program_owner
))

print(ix)
