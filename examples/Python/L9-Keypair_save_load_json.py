import json
from solders.keypair import Keypair


kp = Keypair()
with open("my_wallet.json", "w") as f:
    json.dump(list(bytes(kp)), f)

with open("my_wallet.json") as f:
    data = bytes(json.load(f))
kp2 = Keypair.from_bytes(data)

print("Совпадает:", kp.pubkey() == kp2.pubkey())
