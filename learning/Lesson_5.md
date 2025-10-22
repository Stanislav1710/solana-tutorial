# Урок 5 — Solana CLI: основные команды (keygen, airdrop, balance, transfer)

---

## 1. Введение

**Solana CLI** — это официальный инструмент командной строки, предназначенный для взаимодействия с сетью Solana.  
Он позволяет выполнять те же действия, что и программные клиенты, но напрямую из терминала.

CLI используется для:
- управления кошельками и ключами (Keypair);
- проверки баланса и отправки транзакций;
- подключения к различным сетям (Devnet, Testnet, Mainnet-Beta);
- локального тестирования и быстрой диагностики.

> 📘 Подробная и актуальная документация по установке и использованию находится на официальном сайте Solana:  
> [Solana CLI Tool Suite](https://docs.solanalabs.com/cli)

---

## 2. Роль CLI в экосистеме Solana

`solana-cli` — это интерфейс для взаимодействия с RPC-узлами Solana.  
Все команды CLI под капотом используют те же RPC-запросы, что и любой клиент на Python/JavaScript/TypeScript.

CLI незаменим на этапах:
- отладки и тестирования программ;
- работы с Devnet/Testnet без написания кода;
- генерации кошельков и проверки транзакций;
- развёртывания смарт-контрактов (программ) в Mainnet.

Таким образом, CLI — это инструмент разработчика, а Python/JavaScript/TypeScript — это инструмент интеграции.  
Они используют одну и ту же инфраструктуру Solana.

---

## 3. Основные команды CLI

| Действие | Команда CLI |
|-----------|--------------|
| Создание нового кошелька | `solana-keygen new` |
| Проверка баланса | `solana balance` |
| Получение тестовых SOL | `solana airdrop 1` |
| Перевод SOL | `solana transfer <to> <amount>` |
| Просмотр конфигурации сети | `solana config get` |

---

## 4. Примеры эквивалентов

Используем код из [`examples/Python/L5-CLI_equivalent.py`](../examples/Python/L5-CLI_equivalent.py):

```python
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer

# Подключаемся к devnet
client = Client("https://api.devnet.solana.com")

# 1. Создание нового кошелька (аналог solana-keygen new)
wallet = Keypair()
print("Адрес нового кошелька:", wallet.pubkey())

# 2. Проверка баланса (аналог solana balance)
balance = client.get_balance(wallet.pubkey())
print("Текущий баланс:", balance.value, "lamports")

# 3. Получение тестовых SOL (аналог solana airdrop)
airdrop = client.request_airdrop(wallet.pubkey(), 1000000000)
print("Airdrop Signature:", airdrop.value)

# 4. Перевод SOL (аналог solana transfer)
recipient = Pubkey.from_string("11111111111111111111111111111111")
ix = transfer(TransferParams(from_pubkey=wallet.pubkey(), to_pubkey=recipient, lamports=500000000))
print("Создана инструкция перевода:", ix)
```
**Результат (пример):**
```
Адрес нового кошелька: A9QqHDM6dXbfBhM2Gk7nFtkb9F61BBY8VrEbcATHHyAd
Текущий баланс: 0 lamports
Airdrop Signature: 4YnDK3J9z5Z3pmEDLXtgJv8TBhNZad6afUV8hi1ozDoiZp9ZcmtYrYbei6gKX7d1H3KxmXpYjNtFTBrsKhVf8tDj
Создана инструкция перевода: Instruction { program_id: 11111111111111111111111111111111, accounts: [AccountMeta { pubkey: A9QqHDM6dXbfBhM2Gk7nFtkb9F61BBY8VrEbcATHHyAd, is_signer: true, is_writable: true }, AccountMeta { pubkey: 11111111111111111111111111111111, is_signer: false, is_writable: true }], data: [2, 0, 0, 0, 0, 101, 205, 29, 0, 0, 0, 0] }
```

**Что делает этот код:**
- создаёт новый Keypair (новый кошелёк);
- проверяет баланс через RPC;
- выполняет запрос на получение 1 SOL через Devnet;
- формирует инструкцию для перевода средств.

> Обратите внимание: все эти действия выполняются через один RPC endpoint.  

---

## 5. Практика

1. Перейдите на [официальную страницу CLI](https://docs.solanalabs.com/cli) и установите `solana-cli`.
2. Создайте новый кошелёк с помощью `solana-keygen new`.
3. Проверьте текущий RPC URL через `solana config get`.
4. Получите тестовые SOL в Devnet (`solana airdrop 1`).
5. Повторите эти же шаги с помощью Python/JavaScript/TypeScript-кода из примеров выше.

---

## 6. Вопросы для самопроверки

1. Что делает `solana-cli` и зачем он нужен разработчику?
2. Почему CLI и Python/JavaScript/TypeScript используют одни и те же RPC endpoint’ы?
3. Чем отличается `solana-keygen new` от `Keypair()` в Python?
4. В какой сети доступна команда `solana airdrop`?
5. Почему CLI остаётся важным инструментом даже при наличии SDK?

---

## 7. Навигация

[← Урок 4 — RPC и WebSocket: как клиент общается с цепочкой](Lesson_4.md)  
[→ Урок 6 — solana-test-validator: локальная сеть для разработки](Lesson_6.md)

