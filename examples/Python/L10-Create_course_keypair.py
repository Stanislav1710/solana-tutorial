from solders.keypair import Keypair


course_kp = Keypair()
print("Course pubkey:", course_kp.pubkey())


with open("course_wallet.bin", "wb") as f:
    f.write(bytes(course_kp))

print("Сохранено в course_wallet.bin (64 байта). Добавьте файл в .gitignore для безопасности.")
