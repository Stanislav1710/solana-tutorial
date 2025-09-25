# *********************** ИМПОРТ НЕОБХОДИМЫХ БИБЛИОТЕК **************************
from solana.rpc.api import Client
# *******************************************************************************

# *********************** RPC ДЛЯ ВЫБОРА НЕОБХОДИМОЙ СЕТИ ***********************
RPC_ENDPOINTS = {
    "devnet": "https://api.devnet.solana.com",
    "mainnet": "https://api.mainnet-beta.solana.com",
}
# *******************************************************************************


# ****************🔹 1. ФУНКЦИЯ ДЛЯ ПОДКЛЮЧЕНИЯ К СЕТИ SOLANA *******************
def get_connection(network='devnet') -> Client:
    """
    Подключается к выбранной сети Solana и возвращает объект клиента.

    :param network: str — название сети ("devnet" или "mainnet").
    :return: solana.rpc.api.Client — клиент для взаимодействия с выбранной сетью Solana.
           Этот объект используется для выполнения RPC-запросов, например:
           - client.get_balance(pubkey)
           - client.get_transaction(signature)
           - client.get_account_info(pubkey)
    """
    network = network.lower()
    if network not in RPC_ENDPOINTS:
        raise ValueError(f"Неподдерживаемая сеть '{network}'. Поддерживаются: {list(RPC_ENDPOINTS.keys())}")

    client = Client(RPC_ENDPOINTS[network], timeout=30)
    version = client.get_version()
    print(f"Connected to Solana cluster ({network}):", version)
    return client
# *******************************************************************************


# 🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹 ПРИМЕР ИСПОЛЬЗОВАНИЯ 🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹🔹
if __name__ == "__main__":
    get_connection(network="mainnet")
