from solders.pubkey import Pubkey
from Wallet import load_wallet
from Connect import get_connection
from solana.rpc.types import TokenAccountOpts
from bip_utils import base58
import struct


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
    # Словарь популярных токенов Solana (mainnet)
    MAINNET_TOKENS = {
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": {"symbol": "USDC", "name": "USD Coin"},
        "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {"symbol": "USDT", "name": "Tether USD"},
        "So11111111111111111111111111111111111111112": {"symbol": "wSOL", "name": "Wrapped SOL"},
        "SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt": {"symbol": "SRM", "name": "Serum"},
        "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R": {"symbol": "RAY", "name": "Raydium"},
        "kinXdEcpDQeHPEuQnqmUgtYykqKGVFq6CeVX5iAHJq6": {"symbol": "KIN", "name": "Kin"},
        "MERt85fc5boKw3BW1eYdxonEuJNvXbiMbs6hvheau5K": {"symbol": "MER", "name": "Mercurial"},
        "9n4nbM75f5Ui33ZbPYXn59EwSgE8CGsHtAeTH5YFeJ9E": {"symbol": "BTC", "name": "Bitcoin (Wrapped)"},
        "2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk": {"symbol": "ETH", "name": "Ethereum (Wrapped)"},
        "AGFEad2et2ZJif9jaGpdMixQqvW5i81aBdvKe7PHNfz3": {"symbol": "FTT", "name": "FTX Token"},
    }

    # Devnet токены (если нужно)
    DEVNET_TOKENS = {
        # Добавьте известные devnet токены здесь при необходимости
    }

    token_list = MAINNET_TOKENS if network == "mainnet-beta" else DEVNET_TOKENS
    token_list.update(MAINNET_TOKENS)  # Всегда включаем mainnet токены

    if mint_address in token_list:
        return token_list[mint_address]

    # Если токен не найден в списке, возвращаем сокращенный mint
    return {"symbol": f"{mint_address[:4]}...{mint_address[-4]}", "name": f"Unknown Token"}


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
    except Exception as e:
        print(f"Ошибка парсинга данных аккаунта: {e}")

    return None


def get_spl_tokens(pubkey: Pubkey, network="devnet"):
    """
    Получает список SPL-токенов в кошельке с названиями токенов.
    """
    client = get_connection(network)
    tokens = []

    TOKEN_PROGRAM_ID = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")

    # Убираем encoding="jsonParsed" для совместимости
    resp = client.get_token_accounts_by_owner(
        pubkey,
        TokenAccountOpts(program_id=TOKEN_PROGRAM_ID)
    )

    if resp.value:
        for acc in resp.value:
            try:
                # Получаем mint-адрес из распарсенных данных
                # Используем более надежный способ получения данных аккаунта
                account_info = client.get_account_info(acc.pubkey)
                if account_info.value:
                    # Парсим данные аккаунта вручную
                    mint_address = parse_token_account_data(account_info.value.data)
                    if not mint_address:
                        continue
                else:
                    continue

                # Получаем баланс токена
                balance_resp = client.get_token_account_balance(acc.pubkey)
                if not balance_resp.value:
                    continue

                token_amount = balance_resp.value.ui_amount or 0

                # Получаем информацию о токене
                token_info = get_token_name_by_mint(mint_address, network)

                tokens.append({
                    "mint": mint_address,
                    "name": token_info["name"],
                    "symbol": token_info["symbol"],
                    "amount": token_amount,
                    "account": str(acc.pubkey)
                })

            except Exception as e:
                print(f"Ошибка обработки токен-аккаунта {acc.pubkey}: {e}")
                continue

    return tokens


if __name__ == "__main__":
    wallet = load_wallet("file", "../wallet.json", network="mainnet")

    print("🔹 Баланс кошелька:")
    sol_balance = get_sol_balance(wallet.pubkey(), "mainnet")
    print(f"   SOL: {sol_balance:.5f}")

    spl_balances = get_spl_tokens(wallet.pubkey(), "mainnet")
    if spl_balances:
        print("   SPL токены:")
        for token in spl_balances:
            print(f"    • {token['symbol']} ({token['name']}): {token['amount']}")
    else:
        print("   Нет токенов SPL в кошельке.")