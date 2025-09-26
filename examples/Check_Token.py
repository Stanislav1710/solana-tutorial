from solana.rpc.types import TokenAccountOpts
from solders.solders import Pubkey
from examples.Connect import get_connection
from examples.Wallet import load_wallet


def get_token_balance(pubkey: Pubkey, mint_address: str, network="devnet"):
    """
    Упрощенная функция для получения баланса конкретного токена.
    """
    try:
        client = get_connection(network, debug=False)
        # Создаем фильтр для конкретного токена
        mint_pubkey = Pubkey.from_string(mint_address)

        # Запрос конкретного токен-аккаунта
        resp = client.get_token_accounts_by_owner(
            pubkey,
            TokenAccountOpts(mint=mint_pubkey)
        )

        if resp.value and len(resp.value) > 0:
            # Получаем баланс первого найденного аккаунта
            balance_resp = client.get_token_account_balance(resp.value[0].pubkey)
            if balance_resp.value:
                token_amount = balance_resp.value.ui_amount or 0
                return {
                    "mint": mint_address,
                    "amount": token_amount,
                    "account": str(resp.value[0].pubkey)
                }

        # Если токен не найден, возвращаем нулевой баланс
        return {
            "mint": mint_address,
            "amount": 0.0,
            "account": None
        }
    except Exception as err:
        ...


if __name__ == "__main__":
    wallet = load_wallet("file", "../wallet.json", network="mainnet", get_balance=False)
    wallet_pubkey = wallet.pubkey()

    # Пример получения баланса конкретного токена на примере USDT (упрощенный подход)
    print("\n🔹 Баланс конкретных токенов (упрощенный запрос):")
    usdt_address = 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB'
    print("Запрашиваем баланс USDT...")
    usdt_balance = get_token_balance(wallet_pubkey, usdt_address, "mainnet")
    print(f"USDT: {usdt_balance['amount']}")
