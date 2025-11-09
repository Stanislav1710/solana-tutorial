from solders.instruction import AccountMeta
from solders.pubkey import Pubkey


owner = Pubkey.from_string("11111111111111111111111111111111")
meta_rw_signer = AccountMeta(pubkey=owner, is_signer=True, is_writable=True)
print(meta_rw_signer)
