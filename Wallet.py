# *********************** ИМПОРТ НЕОБХОДИМЫХ БИБЛИОТЕК **************************
import json
from solders.keypair import Keypair
from solana.rpc.api import Client
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip32Slip10Ed25519
)
# *******************************************************************************

# *********************** RPC ДЛЯ ВЫБОРА НЕОБХОДИМОЙ СЕТИ ***********************
RPC_ENDPOINTS = {
    "devnet": "https://api.devnet.solana.com",
    "mainnet": "https://api.mainnet-beta.solana.com",
}
# *******************************************************************************

# ************************** ДОПОЛНИТЕЛЬНЫЕ ПЕРЕМЕННЫЕ **************************
derivation_path = "m/44'/501'/0'/0'"
"""
    Путь m/44'/501'/0'/0' говорит:
    m	    корень (master seed)
    44′	    стандарт BIP‑44
    501′	идентификатор монеты (501 — это Solana)
    0′	    номер аккаунта
    0′	    индекс адреса
    
    То есть, DerivePath("m/44'/501'/0'/0'") — это путь к первому аккаунту в Solana.
"""
# *******************************************************************************


# **********************🔹 1. ФУНКЦИЯ СОЗДАНИЕ КОШЕЛЬКА *************************
def create_wallet(save_to_file=False, filename="wallet.json", words_number=12, hidden_data=True) -> dict:
    """
        Создаёт кошелёк Solana с помощью bip_utils.
        :param save_to_file: сохранять ли в файл
        :param filename: имя файла
        :param words_number: 12 или 24 слова
        :param hidden_data: выводить ли данные кошелька в консоль
        :return: словарь с данными кошелька
    """
    if words_number not in [12, 24]:
        raise ValueError("words_number должен быть 12 или 24")

    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(words_number)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

    bip32_ctx = Bip32Slip10Ed25519.FromSeed(seed_bytes)
    bip32_ctx = bip32_ctx.DerivePath(derivation_path)

    private_key_bytes = bip32_ctx.PrivateKey().Raw().ToBytes()
    kp = Keypair.from_seed(private_key_bytes[:32])  # Phantom использует первые 32 байта

    pubkey = str(kp.pubkey())
    secret_base58 = str(kp)

    if not hidden_data:
        print("Wallet:", pubkey)
        print("Secret key (base58):", secret_base58)
        print(f"Mnemonic ({words_number} words):", mnemonic.ToStr(), "\n")

    if save_to_file:
        data = {
            "public_key": pubkey,
            "secret_key_base58": secret_base58,
            "mnemonic": mnemonic.ToStr()
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Wallet saved to {filename}\n")

    return {
        "public_key": pubkey,
        "secret_key_base58": secret_base58,
        "mnemonic": mnemonic.ToStr()
    }
# *******************************************************************************


# ******************🔹 2. ФУНКЦИЯ  ПОДКЛЮЧЕНИЯ К КОШЕЛЬКУ ***********************
def load_wallet(method: str, value, network="devnet", get_balance=True) -> Keypair:
    """
        Подключение кошелька по методу.
        :param method: "mnemonic" | "base58" | "file"
        :param value: мнемоника, base58 ключ или путь к файлу
        :param network: "devnet" | "mainnet"
        :param get_balance: выводить ли баланс кошелька в консоль
        :return: объект solders.keypair, который хранит пару ключей(приватный + публичный)
    """
    if method == "mnemonic":
        seed_bytes = Bip39SeedGenerator(value).Generate()
        bip32_ctx = Bip32Slip10Ed25519.FromSeed(seed_bytes)

        bip32_ctx = bip32_ctx.DerivePath(derivation_path)
        private_key_bytes = bip32_ctx.PrivateKey().Raw().ToBytes()
        kp = Keypair.from_seed(private_key_bytes[:32])

    elif method == "base58":
        kp = Keypair.from_base58_string(value)

    elif method == "file":
        with open(value, "r") as f:
            data = json.load(f)
        if "mnemonic" in data:
            seed_bytes = Bip39SeedGenerator(data["mnemonic"]).Generate()
            bip32_ctx = Bip32Slip10Ed25519.FromSeed(seed_bytes)
            bip32_ctx = bip32_ctx.DerivePath(derivation_path)
            private_key_bytes = bip32_ctx.PrivateKey().Raw().ToBytes()
            kp = Keypair.from_seed(private_key_bytes[:32])
            method = "file-mnemonic"
        elif "secret_key_base58" in data:
            kp = Keypair.from_base58_string(data["secret_key_base58"])
            method = "file-base58"
        else:
            raise ValueError("Файл не содержит приватного ключа или мнемонической фразы")

    else:
        raise ValueError("Unsupported method. Use mnemonic | base58 | file")

    client = Client(RPC_ENDPOINTS[network.lower()])
    pubkey_obj = kp.pubkey()
    print(f"Connected wallet (method type: {method}):")
    print("Public key:", pubkey_obj)
    print("RPC:", RPC_ENDPOINTS[network.lower()], "\n")
    if get_balance:
        balance_resp = client.get_balance(pubkey_obj)
        lamports = balance_resp.value
        sol = lamports / 1_000_000_000
        print("Balance:", lamports, "lamports =", sol, "SOL")

    return kp
# *******************************************************************************


# 🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹 ПРИМЕР ИСПОЛЬЗОВАНИЯ 🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
if __name__ == "__main__":
    # 1.1 Создать кошелёк с 12 словами
    create_wallet(save_to_file=True, filename="wallet.json", words_number=12, hidden_data=False)

    # 1.2 Создать кошелёк с 24 словами
    # create_wallet(save_to_file=True, filename="wallet.json", words_number=24, hidden_data=False)

    # 2.1 Подключиться к существующему кошельку через файл
    load_wallet("file", "wallet.json", network="mainnet", get_balance=True)

    # 2.2 Подключиться через base58 приватный ключ
    # secret_key = "secret_key"
    # load_wallet("base58", secret_key, network="mainnet")

    # 2.3 Подключиться через мнемонику
    # mnemonic = "mnemonic_phrase"
    # load_wallet("mnemonic", mnemonic, network="mainnet")
