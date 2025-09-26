#######################################################################################################
# данный код еще не учтен в файлах обучения и будет использован для личного ознакомления и тестирования
#######################################################################################################


from solders.pubkey import Pubkey
from Wallet import load_wallet
from Connect import get_connection
from solana.rpc.types import TokenAccountOpts
from bip_utils import base58
import time


def get_sol_balance(pubkey: Pubkey, network="devnet") -> float:
    """
    Получает баланс SOL в кошельке.
    """
    client = get_connection(network)
    resp = client.get_balance(pubkey)
    if resp.value is not None:
        return resp.value / 1_000_000_000  # перевод из лампортов в SOL
    return 0.0


def get_token_name_by_mint(mint_address: str, network="devnet"):
    """
    Получает название токена по его mint-адресу.
    """
    # Расширенный словарь популярных токенов Solana
    MAINNET_TOKENS = {
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {"symbol": "USDC", "name": "USD Coin"},
        "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {"symbol": "USDT", "name": "Tether USD"},
        "So11111111111111111111111111111111111111112": {"symbol": "wSOL", "name": "Wrapped SOL"},
        "SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt": {"symbol": "SRM", "name": "Serum"},
        "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R": {"symbol": "RAY", "name": "Raydium"},
        "kinXdEcpDQeHPEuQnqmUgtYykqKGVFq6CeVX5iAHJq6": {"symbol": "KIN", "name": "Kin"},
        "MERt85fc5boKw3BW1eYdxonEuJNvXbiMbs6hvheau5K": {"symbol": "MER", "name": "Mercurial"},
        "9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E": {"symbol": "BTC", "name": "Wrapped Bitcoin"},
        "2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk": {"symbol": "ETH", "name": "Wrapped Ethereum"},
        "AGFEad2et2ZJif9jaGpdMixQqvW5i81aBdvKe7PHNfz3": {"symbol": "FTT", "name": "FTX Token"},
        "mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So": {"symbol": "mSOL", "name": "Marinade Staked SOL"},
        "7dHbWXmci3dT8UFYWYZweBLXgycu7Y3iL6trKn1Y7ARj": {"symbol": "stSOL", "name": "Lido Staked SOL"},
        "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3": {"symbol": "pSOL", "name": "Parasol"},
        "CWE8jPTUYhdCTZYWPTe1o5DFqfdjzWKc9WKz6rSjQUdG": {"symbol": "LINK", "name": "Chainlink"},
        "HxhWkVpk5NS4Ltg5nij2G671CKXFRKPK8vy271Ub4uEK": {"symbol": "HXRO", "name": "HXRO"},
        "EchesyfXePKdLtoiZSL8pBe8Myagyy8ZRqsACNCFGnvp": {"symbol": "FIDA", "name": "Bonfida"},
        "ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx": {"symbol": "ATLAS", "name": "Star Atlas"},
        "poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk": {"symbol": "POLIS", "name": "Star Atlas DAO"},
        "SLNDpmoWTVADgEdndyvWzroNL7zSi1dF9PC3xHGtPwp": {"symbol": "SLND", "name": "Solend"},
    }

    token_list = MAINNET_TOKENS

    if mint_address in token_list:
        return token_list[mint_address]

    # Если токен не найден в списке, возвращаем сокращенный mint
    return {"symbol": f"{mint_address[:4]}...{mint_address[-4]}", "name": "Unknown Token"}


def parse_token_account_data(data):
    """
    Парсит данные токен-аккаунта и извлекает mint-адрес используя bip_utils.
    """
    try:
        # Данные токен-аккаунта имеют определенную структуру
        # Mint address находится по смещению 0, длина 32 байта
        if len(data) >= 32:
            mint_bytes = data[:32]
            # Используем base58 из bip_utils
            mint_address = base58.Base58Encoder.Encode(mint_bytes)
            return mint_address
    except Exception:
        # Не выводим ошибку парсинга
        pass

    return None


def get_spl_tokens(pubkey: Pubkey, network="devnet", mint_filter=None):
    """
    Получает список SPL-токенов в кошельке.
    """
    try:
        client = get_connection(network)
    except Exception as e:
        print(f"Ошибка подключения к сети: {e}")
        return []

    tokens = []
    successful_count = 0
    error_count = 0

    TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")

    try:
        # Задержка перед первым запросом
        time.sleep(0.2)
        resp = client.get_token_accounts_by_owner(
            pubkey,
            TokenAccountOpts(program_id=TOKEN_PROGRAM_ID)
        )
    except Exception as e:
        print(f"Ошибка при запросе токен-аккаунтов: {e}")
        return tokens

    # Подготовим список для фильтрации
    mint_filter_list = None
    if isinstance(mint_filter, str):
        mint_filter_list = [mint_filter]
    elif isinstance(mint_filter, (list, tuple, set)):
        mint_filter_list = list(mint_filter)

    if not resp.value:
        print("Нет токен-аккаунтов в ответе")
        return tokens

    total_accounts = len(resp.value)
    print(f"Найдено {total_accounts} токен-аккаунтов для обработки")

    for i, acc in enumerate(resp.value):
        try:
            # Задержка между запросами
            if i > 0:
                time.sleep(0.3)

            # Получаем информацию об аккаунте
            account_info = client.get_account_info(acc.pubkey)
            if not account_info.value:
                error_count += 1
                continue

            # Парсим mint-адрес
            mint_address = parse_token_account_data(account_info.value.data)
            if not mint_address:
                error_count += 1
                continue

            # Если фильтр есть — проверяем
            if mint_filter_list and mint_address not in mint_filter_list:
                continue

            # Получаем баланс токена
            balance_resp = client.get_token_account_balance(acc.pubkey)
            if not balance_resp.value:
                error_count += 1
                continue

            token_amount = balance_resp.value.ui_amount or 0

            # Пропускаем токены с нулевым балансом
            if token_amount == 0:
                continue

            # Получаем информацию о токене
            token_info = get_token_name_by_mint(mint_address, network)

            tokens.append({
                "mint": mint_address,
                "name": token_info["name"],
                "symbol": token_info["symbol"],
                "amount": token_amount,
                "account": str(acc.pubkey)
            })

            successful_count += 1

        except Exception:
            # Не выводим ошибку, просто считаем
            error_count += 1
            continue

    # Выводим итоговую статистику
    print(f"Успешно обработано: {successful_count}, с ошибками: {error_count}")

    return tokens


def get_token_balance_simple(pubkey: Pubkey, mint_address: str, network="devnet"):
    """
    Упрощенная функция для получения баланса конкретного токена.
    """
    try:
        # Большая задержка перед запросом
        time.sleep(2)

        client = get_connection(network)

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
                token_info = get_token_name_by_mint(mint_address, network)

                return {
                    "mint": mint_address,
                    "name": token_info["name"],
                    "symbol": token_info["symbol"],
                    "amount": token_amount,
                    "account": str(resp.value[0].pubkey)
                }

        # Если токен не найден, возвращаем нулевой баланс
        token_info = get_token_name_by_mint(mint_address, network)
        return {
            "mint": mint_address,
            "name": token_info["name"],
            "symbol": token_info["symbol"],
            "amount": 0.0,
            "account": None
        }

    except Exception as e:
        # Возвращаем нулевой баланс при ошибке
        token_info = get_token_name_by_mint(mint_address, network)
        return {
            "mint": mint_address,
            "name": token_info["name"],
            "symbol": token_info["symbol"],
            "amount": 0.0,
            "account": None
        }


if __name__ == "__main__":
    wallet = load_wallet("file", "../wallet.json", network="mainnet")
    wallet_pubkey = wallet.pubkey()

    print("🔹 Баланс кошелька:")
    sol_balance = get_sol_balance(wallet_pubkey, "mainnet")
    print(f"   SOL: {sol_balance:.5f}")

    # Получаем все SPL-токены
    print("Получаем список SPL-токенов...")
    spl_balances = get_spl_tokens(wallet_pubkey, "mainnet")

    if spl_balances:
        print("   SPL токены:")
        for token in spl_balances:
            print(f"    • {token['symbol']} ({token['name']}): {token['amount']}")
    else:
        print("   Нет токенов SPL в кошельке.")

    # Пример получения баланса конкретного токена (упрощенный подход)
    print("\n🔹 Баланс конкретных токенов (упрощенный запрос):")

    # USDT - используем упрощенную функцию
    print("Запрашиваем баланс USDT...")
    usdt_balance = get_token_balance_simple(wallet_pubkey, "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", "mainnet")
    print(f"   USDT: {usdt_balance['amount']}")

    # wSOL - используем упрощенную функцию
    print("Запрашиваем баланс wSOL...")
    wsol_balance = get_token_balance_simple(wallet_pubkey, "So11111111111111111111111111111111111111112", "mainnet")
    print(f"   wSOL: {wsol_balance['amount']}")

    # Также покажем баланс USDT из уже полученного списка (если есть)
    if spl_balances:
        usdt_in_list = next((t for t in spl_balances if t['mint'] == "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"),
                            None)
        if usdt_in_list:
            print(f"   USDT (из списка): {usdt_in_list['amount']}")

        wsol_in_list = next((t for t in spl_balances if t['mint'] == "So11111111111111111111111111111111111111112"),
                            None)
        if wsol_in_list:
            print(f"   wSOL (из списка): {wsol_in_list['amount']}")