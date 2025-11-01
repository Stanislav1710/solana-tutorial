from solders.pubkey import Pubkey


system_program = Pubkey.from_string("11111111111111111111111111111111")
print("Тип:", type(system_program))
print("Как строка:", str(system_program))
print("Сырые байты (32):", len(bytes(system_program)))
