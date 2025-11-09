from solders.instruction import Instruction
from solders.pubkey import Pubkey


program_id = Pubkey.from_string("11111111111111111111111111111111")
ix = Instruction(program_id=program_id, accounts=[], data=b"")
print(ix)
