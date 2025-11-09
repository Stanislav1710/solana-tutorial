from solders.pubkey import Pubkey
from solders.system_program import AssignParams, assign


account_pubkey = Pubkey.from_string("11111111111111111111111111111111")
new_owner = Pubkey.from_string("11111111111111111111111111111111")

ix = assign(AssignParams(pubkey=account_pubkey, owner=new_owner))
print(ix)
