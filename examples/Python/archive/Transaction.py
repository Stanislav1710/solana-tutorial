from Wallet import load_wallet
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solders.message import Message

RPC_ENDPOINTS = {
    "devnet": "https://api.devnet.solana.com",
    "mainnet": "https://api.mainnet-beta.solana.com",
}


def send_sol(sender_kp: Keypair, recipient: str, amount_sol: float, network="devnet"):
    """
    Отправляет SOL с одного кошелька на другой.
    """
    client = get_connection(network)

    # Получаем последний blockhash
    blockhash_resp = client.get_latest_blockhash()
    recent_blockhash = blockhash_resp.value.blockhash

    # Инструкция перевода
    ix = transfer(
        TransferParams(
            from_pubkey=sender_kp.pubkey(),
            to_pubkey=Pubkey.from_string(recipient),
            lamports=int(amount_sol * 1_000_000_000)
        )
    )

    # Создаем сообщение
    message = Message.new_with_blockhash(
        [ix],
        sender_kp.pubkey(),
        recent_blockhash
    )

    # Создаем транзакцию
    tx = Transaction.new_unsigned(message)

    # Подписываем транзакцию
    tx.sign([sender_kp], recent_blockhash)

    # Отправляем: попробуем использовать send_transaction, который принимает объект транзакции
    resp = client.send_transaction(tx)
    print(f"✅ Transaction sent! TxID: {resp.value}")
    return resp.value


# 🔹 Пример использования
if __name__ == "__main__":
    wallet = load_wallet("file", "../wallet.json", network="devnet")
    recipient_address = "recipient_address"
    send_sol(wallet, recipient_address, 0.01, network="devnet")

