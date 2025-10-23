from solders.pubkey import Pubkey


pub = Pubkey.from_string("11111111111111111111111111111111")
print("Pubkey:", pub)
print("Как байты:", bytes(pub))
