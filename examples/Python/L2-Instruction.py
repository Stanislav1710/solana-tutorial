from solders.instruction import Instruction, AccountMeta
from solders.pubkey import Pubkey


program_id = Pubkey.from_string("11111111111111111111111111111111")
accounts: list[AccountMeta] = []

ix = Instruction(
    program_id=program_id,
    accounts=accounts,
    data=b""
)

print(ix)
