import subprocess
from solders.keypair import Keypair


decrypted = subprocess.check_output(["gpg", "--decrypt", "course_wallet.bin.gpg"])

kp = Keypair.from_bytes(decrypted)
print("Загруженный pubkey:", kp.pubkey())
