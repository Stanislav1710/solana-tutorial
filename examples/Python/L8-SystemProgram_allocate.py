from solders.pubkey import Pubkey
from solders.system_program import AllocateParams, allocate


account_pubkey = Pubkey.from_string("11111111111111111111111111111111")
ix = allocate(AllocateParams(pubkey=account_pubkey, space=128))
print(ix)
