# Урок 7 — Знакомство с SOLANA: возможности, уровни API

---

## 1. Введение

Библиотека **`solana`** — это официальный Python‑клиент для работы с сетью Solana через RPC и WebSocket.  
Его задача — дать **удобный высокоуровневый интерфейс**: выполнять запросы, собирать и отправлять транзакции, читать аккаунты.

В этом уроке мы разберём:
- из чего состоит `solana` и чем он отличается от `solders`;
- как правильно создавать клиент и делать запросы;
- как задавать уровни подтверждения (commitment) и опции RPC;
- как читать аккаунты и получать блокхеш;
- как подготовить минимальную транзакцию (без реальной отправки);
- **множество небольших примеров** для закрепления.

> Версии, на которых основаны примеры: `solana==0.36.9`, `solders==0.26.0`.

---

## 2. `solana` vs `solders` — в чём разница

| Критерий | `solana` (Python SDK) | `solders` (низкоуровневые типы) |
|---|---|---|
| Назначение | Высокоуровневые клиенты и удобные вызовы RPC | Быстрые строгие структуры и типы (Pubkey, Keypair, Instruction и др.) |
| Где используется | `solana.rpc.api.Client`, helpers, WebSocket клиент | Конструирование сообщений/инструкций, ключей, транзакций |
| Производительность | Удобно | Быстро и строго |
| Что выбирать | Для 80% клиентских задач | Для сборки транзакций и точных типов |

> На практике они **используются вместе**: `solana` делает запросы, `solders` даёт типы и конструкторы инструкций.

---

## 3. Устройство библиотеки `solana`

Минимальный набор модулей, с которыми вы будете работать:

- `solana.rpc.api.Client` — HTTP JSON‑RPC клиент (основа большинства операций).
- `solana.rpc.websocket_api` — WebSocket API (подписки на события).
- `solana.rpc.types` — вспомогательные типы для опций запросов.
- `solders.*` — ключи, транзакции, инструкции и т.д.


---

## 4. Создание клиента и базовые запросы

### 4.1. Подключение к Devnet и проверка связи

Используем код из [`examples/Python/L7-Intro_solana.py`](../examples/Python/L7-Intro_solana.py):

```python
from solana.rpc.api import Client

# Создаём клиент к Devnet
client = Client("https://api.devnet.solana.com")

# Проверяем подключение (ping через getHealth)
print("Подключено:", client.is_connected())

# Узнаём номер текущего слота
print("Текущий слот:", client.get_slot().value)

# Версия RPC ноды
print("RPC версия:", client.get_version().value.solana_core)
```

**Пояснение:** `Client` управляет HTTP‑соединением и сериализацией JSON‑RPC.

---

### 4.2. Настройка уровня подтверждения (commitment)

**Commitment** — это «насколько надёжный срез состояния» вы запрашиваете у RPC-узла.  
Solana параллельно обрабатывает множество транзакций; данные могут меняться каждую миллисекунду. Commitment позволяет выбрать баланс между **скоростью** и **финальной гарантией**:

- **`processed`** — самый быстрый снимок: узел увидел транзакцию/изменение и обработал его локально. Подходит для «живых» UI, индикаторов прогресса.
- **`confirmed`** — данные подтверждены большинством валидаторов в недавнем блоке. Компромисс между скоростью и надёжностью.
- **`finalized`** — максимально надёжный срез: блок закреплён супермажорити валидаторов. Используйте для критичных показов состояния (например, итоговые балансы, бухгалтерия).

Используем код из [`examples/Python/L7-Commitment_options.py`](../examples/Python/L7-Commitment_options.py):

```python
from solana.rpc.api import Client, Commitment


client = Client("https://api.devnet.solana.com")

# Запрос с явным commitment: finalized
slot_finalized = client.get_slot(commitment=Commitment("finalized")).value
print("Слот (finalized):", slot_finalized)

# Запрос с более «быстрым» срезом состояния: processed
slot_processed = client.get_slot(commitment=Commitment("processed")).value
print("Слот (processed):", slot_processed)
```
Ещё пара практических примеров с commitment:

Используем код из [`examples/Python/L7-Commitment_balance_and_status.py`](../examples/Python/L7-Commitment_balance_and_status.py):

```python
from solana.rpc.api import Client, Commitment
from solders.pubkey import Pubkey

client = Client("https://api.devnet.solana.com")
address = Pubkey.from_string("11111111111111111111111111111111")

# Баланс с разными уровнями
b_fast = client.get_balance(address, commitment=Commitment("processed")).value
b_safe = client.get_balance(address, commitment=Commitment("finalized")).value
print("Баланс (processed):", b_fast)
print("Баланс (finalized):", b_safe)
```

#### Когда какой уровень выбирать

- **UI/потоковые обновления:** `processed`/`confirmed` — быстрее реагирует, достаточно для индикации.
- **Итоги и отчёты:** `finalized` — когда важно исключить откаты.
- **Проверка статуса подписи:** сначала `processed` (быстрая реакция), затем повторная проверка `finalized` перед фиксацией результата в вашей БД.

---

### 4.3. Получение баланса и информации об аккаунте

Используем код из [`examples/Python/L7-Get_balance_and_account.py`](../examples/Python/L7-Get_balance_and_account.py):

```python
from solana.rpc.api import Client
from solders.pubkey import Pubkey


client = Client("https://api.devnet.solana.com")

system_program = Pubkey.from_string("11111111111111111111111111111111")

# Баланс (lamports)
balance_resp = client.get_balance(system_program)
print("Баланс:", balance_resp.value)

# Информация об аккаунте
info_resp = client.get_account_info(system_program)
print("Executable:", info_resp.value.executable)
print("Owner:", info_resp.value.owner)
```

> Возвращаемые объекты (`GetBalanceResp`, `GetAccountInfoResp` и т.д.) имеют свойство `.value` с полезными данными.

---

### 4.4. Получение последнего блокхеша (для будущих транзакций)

Любая транзакция должна ссылаться на актуальный `recent_blockhash`.

Используем код из [`examples/Python/L7-Latest_blockhash.py`](../examples/Python/L7-Latest_blockhash.py):

```python
from solana.rpc.api import Client

client = Client("https://api.devnet.solana.com")
latest = client.get_latest_blockhash().value
print("blockhash:", latest.blockhash)
print("last_valid_block_height:", latest.last_valid_block_height)
```

> Этот блокхеш мы будем использовать в уроках про транзакции (см. уроки 14–20).

---

## 5. Работа с ключами и адресами (через `solders`)

Ключи в Solana — это **основа всей безопасности**.  
Каждый пользователь, программа или аккаунт идентифицируется уникальной **парой ключей**:
- **публичный ключ (Public Key / Pubkey)** — это ваш адрес в сети, его можно показывать всем;
- **приватный ключ (Secret Key)** — это ваша подпись, используемая для авторизации транзакций.

---

### 5.1. Что такое `Keypair`

Класс `Keypair` из `solders.keypair` — это объект, содержащий оба ключа: приватный и публичный.  
Он основан на криптосхеме **Ed25519**, обеспечивающей:
- короткие подписи и ключи (32 байта);
- высокую скорость подписи и проверки;
- стойкость на уровне современных блокчейнов.

Генерация выполняется случайным образом при каждом вызове конструктора:

Используем код из [`examples/Python/L7-Generate_keypair.py`](../examples/Python/L7-Generate_keypair.py):

```python
from solders.keypair import Keypair

# Генерация новой пары
kp = Keypair()
print("Публичный ключ:", kp.pubkey())
print("Приватный ключ (bytes):", kp.secret())
```

**Что происходит:**
- при создании `Keypair()` библиотека случайно генерирует 32-байтное число (seed);
- из него вычисляется публичный ключ с помощью Ed25519;
- пара хранится в памяти и может использоваться для подписи.

> ⚠️ Никогда не публикуйте `kp.secret()` — это доступ к вашим средствам.

---

### 5.2. Публичный ключ (`Pubkey`)

Класс `Pubkey` из `solders.pubkey` представляет адрес аккаунта.  
В Solana **всё — это аккаунты**, и каждый аккаунт имеет Pubkey.

Публичный ключ кодируется в **base58** — это строка из 44 символов без двоичных данных и пробелов, удобная для копирования.

Используем код из [`examples/Python/L7-Pubkey_example.py`](../examples/Python/L7-Pubkey_example.py):

```python
from solders.pubkey import Pubkey

pub = Pubkey.from_string("11111111111111111111111111111111")
print("Pubkey:", pub)
print("Как байты:", bytes(pub))
```

---

### 5.3. Связь между `Keypair` и `Pubkey`

Каждый `Keypair` содержит `pubkey()` — это «открытая часть» пары.  
Например:

```python
kp = Keypair()
address = kp.pubkey()
print("Адрес кошелька:", address)
```

> То, что в Solana называют “адресом аккаунта” — это именно **Pubkey**.

---

### 5.4. Сохранение и восстановление ключей

Solana CLI сохраняет ключи в JSON-файлы (обычно `~/.config/solana/id.json`).  
Вы можете сериализовать свой ключ вручную:

Используем код из [`examples/Python/L7-Save_and_load_keypair.py`](../examples/Python/L7-Save_and_load_keypair.py):

```python
import json
from solders.keypair import Keypair

# Создание нового ключа
kp = Keypair()
print("Адрес:", kp.pubkey())

# Сохраняем пару ключей private + public (64 байта)
full_bytes = bytes(kp)
with open("my_wallet.json", "w") as f:
    json.dump(list(full_bytes), f)
print("Ключ сохранён в my_wallet.json")

# Загружаем обратно
with open("my_wallet.json", "r") as f:
    loaded_bytes = bytes(json.load(f))

kp2 = Keypair.from_bytes(loaded_bytes)
print("Восстановленный адрес:", kp2.pubkey())
```

---

### 5.5. Program ID и отличие от обычного адреса

Программы (смарт-контракты) тоже имеют Pubkey, но их ключи — это **идентификаторы кода**, а не кошельки с балансом.

| Тип адреса | Пример | Что обозначает |
|-------------|--------|----------------|
| Аккаунт пользователя | `8vNdrb3V...WZ4` | Кошелёк с SOL / токенами |
| Program ID | `11111111111111111111111111111111` | Системная программа |
| PDA (Program Derived Address) | `3zQ8kH2n...9iR` | Адрес, созданный программой из seed |

---

### 5.6. Почему base58

Base58 используется, потому что:
- не содержит похожих символов (`0`, `O`, `l`, `I`);
- не требует префиксов вроде `0x`;
- короче, чем hex (32 байта → 44 символа);
- легко вставляется в CLI и веб-интерфейсы.

---

### 5.7. Практическое резюме

- Любая операция в Solana начинается с **Keypair** — он нужен для подписи.  
- Ваш адрес в сети — это **Pubkey**, производный от приватного ключа.  
- Никогда не храните `Keypair` в открытом виде — используйте зашифрованные файлы или переменные окружения.  
- Program ID — это тоже `Pubkey`, но он принадлежит коду программы, а не пользователю.

---

## 6. Минимальный конвейер подготовки транзакции (без отправки)

В этом примере мы **ничего не отправляем**, только собираем структуру — чтобы увидеть, как `solana` и `solders` работают вместе.

Используем код из [`examples/Python/L7-Tx_pipeline_dry_run.py`](../examples/Python/L7-Tx_pipeline_dry_run.py):

```python
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.message import Message
from solders.transaction import Transaction

client = Client("https://api.devnet.solana.com")
sender = Keypair()  # новый кошелёк БЕЗ средств (только для демонстрации)
recipient = Pubkey.from_string("11111111111111111111111111111111")

# 1) Инструкция перевода (1000 lamports)
ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports=1000))

# 2) Получаем актуальный блокхеш
recent_blockhash = client.get_latest_blockhash().value.blockhash

# 3) Формируем сообщение
message = Message.new_with_blockhash([ix], sender.pubkey(), recent_blockhash)

# 4) Создаём транзакцию и подписываем (локально)
tx = Transaction([sender], message, recent_blockhash)
tx.partial_sign([sender], recent_blockhash)

# 5) Не отправляем! Просто печатаем сериализованный размер
raw = bytes(tx)
print("Tx bytes:", len(raw), "байт")
```

> ⚠️ **Предупреждение:** у нового кошелька **нет баланса**, поэтому реальная отправка завершится ошибкой *AccountNotFound*. Здесь мы только показываем **структуру**.

---

## 7. Полезные приёмы при работе с RPC

Работая с сетью Solana через RPC, важно не просто выполнять запросы, а делать это **эффективно**.  
Когда приложение работает с десятками аккаунтов или транзакций, одиночные вызовы становятся медленными и неэффективными.  
Для таких случаев Solana предоставляет **пакетные запросы (batched RPC)** и **проверку статуса транзакций**.

---

### 7.1. Пакетные запросы (get_multiple_accounts)

Когда нужно получить данные сразу по нескольким аккаунтам, гораздо быстрее сделать **один** запрос, чем отправлять десять отдельных.  
Это особенно полезно при:
- чтении состояния токенов нескольких пользователей;
- проверке PDA, связанных с одной программой;
- обновлении интерфейса с данными разных аккаунтов.

RPC-метод `get_multiple_accounts` позволяет передать список ключей и получить все результаты одним вызовом.

Используем код из [`examples/Python/L7-Multiple_accounts.py`](../examples/Python/L7-Multiple_accounts.py):

```python
from solana.rpc.api import Client
from solders.pubkey import Pubkey

client = Client("https://api.devnet.solana.com")

# Список аккаунтов для пакетного запроса
keys = [
    Pubkey.from_string("11111111111111111111111111111111"),  # System Program
    Pubkey.from_string("SysvarRent111111111111111111111111111111111"),  # Rent sysvar
]

# Один запрос вместо двух
resp = client.get_multiple_accounts(keys)

for i, acc in enumerate(resp.value):
    print(f"Аккаунт {i + 1}:")
    print("  Executable:", acc.executable)
    print("  Owner:", acc.owner)
    print("  Data length:", len(acc.data))
```

**Преимущества:**
- экономия пропускной способности RPC;
- меньшая задержка (один round-trip вместо нескольких);
- идеально подходит для UI и индексеров.

---

### 7.2. Проверка статуса транзакции (get_signature_statuses)

После отправки транзакции сеть возвращает **signature** — хэш подписи.  
Чтобы узнать, была ли она успешно обработана, можно вызывать метод `get_signature_statuses`.  
Это нужно для:
- отслеживания статуса отправленных транзакций;
- контроля массовых выплат или аирдропов;
- журналирования успешных и неудачных операций.

Используем код из [`examples/Python/L7-Get_signature_status.py`](../examples/Python/L7-Get_signature_status.py):

```python
from solana.rpc.api import Client
from solders.signature import Signature

client = Client("https://api.devnet.solana.com")

# Список нескольких сигнатур (можно до ~256 за один запрос)
# Список сигнатур должен быть не устаревшим (на момент запуска) для успешного считывания информации
signatures = [
    Signature.from_string("Qu7MpMvUeY7jDUB1F8LhiDQqckFH3p6BdDP69MEFMdSf7tk6NZiU8Em83F26tr9tHMy1woxwx12ohdeTvJAWQHm"),
    Signature.from_string("3hKzDKm7aJhQKD3F55sa1DTJkxQ3VGdrw5tSJ63gLkhRx2xYctdW4gPam91ttqofLFqAEjW1GghqKrmxvjZPUBqk"),
    Signature.from_string("A4YregcmZLG6gmtwF87THMzhcygp2EZyR7Fz5NYyQQutdizxcXjZu8AVKKxQnen56C5XLvPskts244M1jFh8be2")
]

resp = client.get_signature_statuses(signatures)

for i, s in enumerate(resp.value):
    sig = signatures[i]
    print(f"\nСигнатура {i + 1}: {sig}")

    if s is None:
        print("  Статус не найден (возможно, транзакция слишком старая)")
        continue

    # Выводим ключевые поля
    print("  Slot:", s.slot)
    print("  Confirmations:", s.confirmations)
    print("  Status:", s.status)
    print("  Err:", s.err)
    print("  Confirmation status:", s.confirmation_status)

```

**Что возвращается:**
- количество подтверждений (`confirmations`);
- блок (`slot`), в котором выполнена транзакция;
- ошибки, если они были;
- отметка о финальном статусе.

**Пример вывода:**
```
Сигнатура 1: Qu7MpMvUeY7jDUB1F8LhiDQqckFH3p6BdDP69MEFMdSf7tk6NZiU8Em83F26tr9tHMy1woxwx12ohdeTvJAWQHm
  Slot: 416649327
  Confirmations: None
  Status: None
  Err: None
  Confirmation status: TransactionConfirmationStatus.Finalized

Сигнатура 2: 3hKzDKm7aJhQKD3F55sa1DTJkxQ3VGdrw5tSJ63gLkhRx2xYctdW4gPam91ttqofLFqAEjW1GghqKrmxvjZPUBqk
  Slot: 416649327
  Confirmations: None
  Status: None
  Err: None
  Confirmation status: TransactionConfirmationStatus.Finalized

Сигнатура 3: A4YregcmZLG6gmtwF87THMzhcygp2EZyR7Fz5NYyQQutdizxcXjZu8AVKKxQnen56C5XLvPskts244M1jFh8be2
  Slot: 416649327
  Confirmations: None
  Status: TransactionErrorInstructionError((4, Tagged(Custom(InstructionErrorCustom(6010)))))
  Err: TransactionErrorInstructionError((4, Tagged(Custom(InstructionErrorCustom(6010)))))
  Confirmation status: TransactionConfirmationStatus.Finalized
```

---

### 7.3. Практическое применение

| Сценарий | Что использовать | Почему |
|-----------|------------------|---------|
| Отображение нескольких балансов в UI | `get_multiple_accounts` | Один запрос вместо десятков — быстрее интерфейс |
| Проверка нескольких транзакций после массовой отправки | `get_signature_statuses` | Централизованный контроль успешности |
| Проверка PDA и служебных аккаунтов | `get_multiple_accounts` | Быстрая проверка состояния связанных аккаунтов |

> 💡 Эти методы особенно важны для **индексеров**, **мониторингов**, **аналитических сервисов** и **dApp-интерфейсов**.  
> Они уменьшают нагрузку на RPC, ускоряют обновление данных и позволяют масштабировать приложение без изменения логики.

---

## 8. Частые ошибки и как их распознать

| Симптом | Причина | Что делать |
|---|---|---|
| `AccountNotFound` при отправке | Пытаетесь списать со «свежего» кошелька без средств | Сделайте `request_airdrop()` в Devnet или используйте кошелёк с балансом |
| `BlockhashNotFound` | Устарел `recent_blockhash` | Получите новый через `get_latest_blockhash()` и пересоберите транзакцию |
| `Transaction too large` | Слишком много инструкций/подписей | Разбейте операцию на несколько транзакций |
| `Custom program error` | Ошибка логики вашей программы | Смотрите `simulate_transaction()` и логи |

> Для «сухого прогона» используйте `client.simulate_transaction(tx)` — это покажет логи выполнения без записи в блокчейн.

---

## 9. Практика

1. Подключитесь к Devnet и выведите версию RPC ноды и текущий слот.
2. Получите `latest_blockhash` и распечатайте его вместе с `last_valid_block_height`.
3. Сформируйте инструкцию перевода на 1000 лампортов (без отправки) и сериализуйте транзакцию в байты.
4. Считайте данные двух системных аккаунтов одним вызовом `get_multiple_accounts` и сравните поля `owner` и `executable`.

---

## 10. Вопросы для самопроверки

1. Чем `solana` отличается от `solders` и почему их используют вместе?
2. Зачем нужен `recent_blockhash` и где его взять?
3. Что такое `commitment` и как он влияет на ответы RPC?
4. Почему нельзя отправить транзакцию от нового кошелька без баланса?
5. В каких случаях стоит использовать `get_multiple_accounts`?

---

## 11. Навигация

[← Урок 6 — solana-test-validator: локальная сеть для разработки](Lesson_6.md)  
[→ Урок 8 — Знакомство с solders: типы, ключи, структуры](Lesson_8.md)
