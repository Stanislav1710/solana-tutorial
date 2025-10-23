import json
from solders.keypair import Keypair


kp = Keypair()
print("Адрес:", kp.pubkey())

full_bytes = bytes(kp)
with open("my_wallet.json", "w") as f:
    json.dump(list(full_bytes), f)
print("Ключ сохранён в my_wallet.json")

with open("my_wallet.json", "r") as f:
    loaded_bytes = bytes(json.load(f))

kp2 = Keypair.from_bytes(loaded_bytes)
print("Восстановленный адрес:", kp2.pubkey())
