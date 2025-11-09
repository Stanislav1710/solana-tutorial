# Урок 8 — Знакомство с `solders`: строгие типы и структуры Solana

---

## 1. Введение

Библиотека `solders` — это низкоуровневая Python‑обёртка над ключевыми структурами **Solana SDK** (реализованными на Rust).  
Её задача — дать строгие и быстрые типы данных (ключи, подписи, инструкции, транзакции), которые **побитово** совпадают с тем, что обрабатывают валидаторы Solana.  
Если библиотека `solana` отвечает за сетевое взаимодействие (RPC/WebSocket), то `solders` — за **правильную бинарную форму** данных, которые вы собираетесь отправить в сеть. *(см. Урок 7 — «Работа с библиотекой `solana` и RPC»; Урок 4 — «RPC и WebSocket»)*

Почему это важно:
- Любая ошибка в байтах транзакции = неверная подпись = отказ узла выполнять операцию.
- Строгие типы (`Pubkey`, `Signature`, `Instruction`, `Transaction`) защищают от логических ошибок (например, случайно подставить строку вместо ключа).
- Производительность: кодирование/декодирование выполняется нативным Rust‑кодом.

---

## 2. Почему `solders` критичен для Python‑разработчика

1) **Совместимость с сетью.** Формат транзакций и подписей в Solana — строго определён. `solders` повторяет его 1:1.  
2) **Скорость.** Сериализация и хэширование выполняются нативно; это ощутимо при сборке больших транзакций, батчах, индексерах.  
3) **Безошибочность интерфейсов.** Каждый тип (например, `Pubkey`) — отдельный класс. IDE и статический анализ видят неправильные типы ещё до запуска.  
4) **Единый слой для всех SDK.** Rust → Python через `solders` = минимум расхождений в поведении.

Практический вывод: `solana` — для общения с RPC, `solders` — для сборки «правильных байтов». В реальных проектах они используются **вместе**.

---

## 3. Основные структуры `solders` и как они связаны между собой

| Класс | Что описывает | Где применяется |
|---|---|---|
| `Pubkey` | Публичный ключ (адрес аккаунта/программы), ровно 32 байта | идентификация аккаунтов, владельцев, программ |
| `Keypair` | Пара ключей (приватный + публичный), 64 байта в сериализованном виде | подпись транзакций, владение активами |
| `Signature` | Подпись Ed25519, 64 байта | подтверждение транзакций и сообщений |
| `AccountMeta` | Роль аккаунта в инструкции | задаёт `is_signer`, `is_writable` для программы |
| `Instruction` | Описание одного вызова программы | содержит `program_id`, `accounts`, `data` |
| `Message` | Контейнер набора инструкций + payer и пр. | то, что реально подписывается | 
| `Transaction` | Подписанное `Message` + подписи | то, что отправляется в сеть |
| `System Program` | Набор встроенных инструкций | переводы SOL, create_account, allocate и др. |

Поток данных: **Instruction → Message → Transaction → bytes(tx) → RPC**.

---

## 4. `Pubkey` — адреса аккаунтов и программ

### 4.1. Что такое `Pubkey`
`Pubkey` — это 32‑байтовый публичный ключ. В интерфейсе пользователя он обычно отображается как строка **base58** (пример: `9xQeWvG816bUx9EPjHmaT2z9nF7wG...`).  
Base58 удобен: короче hex, без неоднозначных символов (`0/O`, `I/l`), копируется без префиксов.

Используем код из [`examples/Python/L8-Pubkey_intro.py`](../examples/Python/L8-Pubkey_intro.py):
```python
from solders.pubkey import Pubkey

# Создаём Pubkey из base58-строки
system_program = Pubkey.from_string("11111111111111111111111111111111")
print("Тип:", type(system_program))
print("Как строка:", str(system_program))
print("Сырые байты (32):", len(bytes(system_program)))
```

### 4.2. Где используется `Pubkey`
- адреса кошельков пользователей;  
- адреса программ (Program ID);  
- системные счета (например, `SysvarRent...`);  
- PDA (Program Derived Address) — адреса, производные от seed’ов программ. *(см. Урок 27 — «PDA: концепт и использование»)*

### 4.3. Типовые ошибки и защита
- **Ошибка:** передать обычную строку вместо `Pubkey` → программа ожидает 32 байта.  
- **Защита:** в коде используйте `Pubkey` (строгий тип), а не строку — это ловится раньше.

---

## 5. `Keypair` — от генерации до безопасного хранения

### 5.1. Что такое `Keypair`
`Keypair` — это объект, содержащий **приватный** и **публичный** ключ, имеющий:
- приватную часть (seed 32 байта + расширенный секрет для подписи);
- публичную часть (32 байта);  
- сериализованный вид **64 байта**: [секрет (32) + публичный (32)].

Используем код из [`examples/Python/L8-Keypair_intro.py`](../examples/Python/L8-Keypair_intro.py):
```python
from solders.keypair import Keypair

kp = Keypair()  # криптографически стойкая случайная генерация
print("Адрес:", kp.pubkey())
print("Секрет+паблик (64 байта):", len(bytes(kp)))
```

### 5.2. Сохранение/восстановление (правильно!)
**Нельзя** сохранять только `kp.secret()` (32 байта) и потом пытаться сделать `Keypair.from_bytes(32)` — потребуется **64 байта**.

Используем код из [`examples/Python/L8-Keypair_save_load.py`](../examples/Python/L8-Keypair_save_load.py):
```python
import json
from solders.keypair import Keypair

# Сохранение полной пары (64 байта)
kp = Keypair()
with open("my_wallet.json", "w") as f:
    json.dump(list(bytes(kp)), f)

# Загрузка
with open("my_wallet.json") as f:
    raw = bytes(json.load(f))
kp2 = Keypair.from_bytes(raw)
print("Совпадает:", kp.pubkey() == kp2.pubkey())
```

### 5.3. Безопасность
- Не храните ключи **в открытом виде** в репозиториях/логах.
- Шифруйте файлы ключей на диске; ограничивайте доступ правами ОС.
- Для production — аппаратные ключи/внешние KMS (урок 49 далее).

### 5.4. Импорт ключа
Если у вас есть 64 байта — используйте `Keypair.from_bytes(bytes_64)`.  
Если у вас seed‑фраза (mnemonic) — преобразуйте её во внутренний ключ вне `solders` и затем инициализируйте `Keypair` (подробно в уроках 9–10). *(см. также: Урок 10 — «Seed / восстановление и импорт», Урок 9 — «Генерация Keypair»)*

---

## 6. Signature — как читать статус подписанной транзакции

`Signature` — это 64‑байтовый идентификатор транзакции (Ed25519), по которому мы проверяем **успех/ошибку** выполнения и уровень подтверждения. В продакшн‑коде сигнатуры логируются и служат первичным ключом для отслеживания операций. *(см. также: Урок 7 — «Commitment и статусы»; Урок 15 — «Commitment levels»)*

### 6.1. Получаем Signature при отправке и проверяем статус

Примечание. Пример демонстрационный. Если у плательщика нет SOL, реальная отправка завершится ошибкой preflight. Для «живой» проверки используйте известную сигнатуру реальной транзакции (см. 6.2). *(см. также: Урок 14 — «Перевод SOL: сборка и подтверждение»)*

Используем код из [`examples/Python/L8-Signature_status_check.py`](../examples/Python/L8-Signature_status_check.py):
```python
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message

client = Client("https://api.devnet.solana.com")

sender = Keypair()  # пустой счёт, только для структуры
recipient = Pubkey.from_string("11111111111111111111111111111111")

ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports=1000))
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], sender.pubkey(), rbh)

# Подписание и попытка отправки
tx = Transaction([sender], msg, rbh)
tx.partial_sign([sender], rbh)
resp = client.send_transaction(tx)

sig = resp.value  # solders.signature.Signature
print("Подпись транзакции:", sig)

# Проверка статуса
st = client.get_signature_statuses([sig]).value[0]
if st is None:
    print("Статус: не найден (слишком старая/не прошла preflight/ещё в кеше RPC)")
else:
    print("Slot:", st.slot)
    print("Confirmations:", st.confirmations)
    print("Err:", st.err)
    print("Confirmation status:", st.confirmation_status)
    print("Результат:", "Ok(())" if st and st.err is None else f"Err({st.err})")  # Ok(()) или Err(...)
```

---

## 7. `AccountMeta` — роли аккаунтов в инструкции

Каждая программа должна знать, **с какими аккаунтами она работает** и **какие права** ей даны. За это отвечает список `AccountMeta` в инструкции. *(см. также: Урок 2 — «Основные сущности: аккаунты, программы, инструкции, транзакции»)*

Поля `AccountMeta`:
- `pubkey` — адрес аккаунта;
- `is_signer` — требуется ли подпись владельца этого аккаунта;  
- `is_writable` — можно ли изменять лампорты/данные аккаунта.

Почему важно:
- Если аккаунт не пометить `is_writable=True`, программа не сможет изменить его состояние (ошибка исполнения).
- Если требуется подпись, но `is_signer=False`, транзакция будет отвергнута при проверке подписей.

Используем код из [`examples/Python/L8-AccountMeta_example.py`](../examples/Python/L8-AccountMeta_example.py):
```python
from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

owner = Pubkey.from_string("11111111111111111111111111111111")
meta_rw_signer = AccountMeta(pubkey=owner, is_signer=True, is_writable=True)
print(meta_rw_signer)
```

---

## 8. `Instruction` — формируем действие

Инструкция = `program_id` + список `AccountMeta` + `data` (байты).  
`data` — это параметры вызова, закодированные программой (часто Borsh — см. уроки 29–32; Anchor‑совместимость — см. Урок 30).

Используем код из [`examples/Python/L8-Instruction_minimal.py`](../examples/Python/L8-Instruction_minimal.py):
```python
from solders.instruction import Instruction
from solders.pubkey import Pubkey

program_id = Pubkey.from_string("11111111111111111111111111111111")
ix = Instruction(program_id=program_id, accounts=[], data=b"")
print(ix)
```

> **Важно:** сама по себе инструкция **ничего не выполняет**. Она должна быть включена в `Message`, а потом — в `Transaction`.

---

## 9. `Message` и `Transaction` — от описания к подписи и отправке

### 9.1. `Message`
`Message` собирает **упорядоченный список инструкций** и фиксирует **плательщика комиссии (payer)**.  
Именно `Message` подписывается ключами отправителей. *(см. также: Урок 2 — роли сущностей; Урок 19 — «Durable Nonce»)*

Используем код из [`examples/Python/L8-Message_compile.py`](../examples/Python/L8-Message_compile.py):
```python
from solders.message import Message
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client

client = Client("https://api.devnet.solana.com")
sender = Keypair()
recipient = sender.pubkey()
ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=recipient, lamports=1))
recent_blockhash = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], sender.pubkey(), recent_blockhash)
print(msg)
```

### 9.2. `Transaction`
`Transaction` = `Message` + подписи. После подписи транзакцию можно сериализовать в байты и отправить через RPC. *(см. также: Урок 14 — «Перевод SOL: сборка и подтверждение»; Урок 15 — «Commitment levels»)*

Используем код из [`examples/Python/L8-Transaction_sign_only.py`](../examples/Python/L8-Transaction_sign_only.py):
```python
from solders.transaction import Transaction
from solders.keypair import Keypair
from solana.rpc.api import Client
from solders.message import Message
from solders.system_program import transfer, TransferParams

client = Client("https://api.devnet.solana.com")
sender = Keypair()  # Без баланса! Только структура
ix = transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=sender.pubkey(), lamports=1))
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], sender.pubkey(), rbh)

# Формирование и локальная подпись
tx = Transaction([sender], msg, rbh)
tx.partial_sign([sender], rbh)
print("Размер tx в байтах:", len(bytes(tx)))
print(tx)
```

> **Важно:** У этого кошелька нет баланса — реальная отправка закончится ошибкой `AccountNotFound`. Здесь мы показываем **структуру** и процесс подписи. *(см. также: Урок 13 — «Airdrop и баланс через RPC»)*

---

## 10. System Program — каталог базовых инструкций

`System Program` — это встроенная программа Solana (адрес `11111111111111111111111111111111`), которая управляет базовыми операциями на уровне системы: созданием аккаунтов, переводами, выделением памяти и назначением владельцев. Это фундамент Solana — без System Program невозможны даже самые простые транзакции. *(см. также: Урок 2 — «Основные сущности Solana»)*

---

### 10.1. Перевод SOL (`transfer`)
Инструкция **`transfer`** выполняет перевод лампортов между двумя **system-owned аккаунтами**.  
Это базовая операция перемещения SOL в сети Solana.

#### Принцип работы:
- Отправитель (`from_pubkey`) подписывает транзакцию и теряет указанное количество лампортов.  
- Получатель (`to_pubkey`) получает эти лампорты.  
- System Program проверяет, что отправитель существует, подписан и имеет достаточный баланс.  
- При необходимости создаёт запись о получателе (если тот не программа).

#### Пример
Используем код из [`examples/Python/L8-SystemProgram_transfer.py`](../examples/Python/L8-SystemProgram_transfer.py):
```python
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer

sender = Keypair()
recipient = Pubkey.from_string("11111111111111111111111111111111")

ix = transfer(TransferParams(
    from_pubkey=sender.pubkey(),
    to_pubkey=recipient,
    lamports=5000
))

print(ix)
```

#### Когда используется  
- Переводы между пользователями.  
- Пополнение PDA-аккаунтов программ (Program Derived Address — см. Урок 27).  
- Передача лампортов в смарт-контракт как депозит.

#### Ограничения  
- Получатель не может быть `executable`.  
- Отправитель обязан быть подписантом.  
- У отправителя должен быть баланс ≥ сумме перевода + комиссия.  
- Ошибка `ReadonlyLamportChange` — если программа пытается изменить баланс read-only аккаунта.

---

### 10.2. Создание аккаунта (`create_account`)

Инструкция **`create_account`** создаёт новый аккаунт в блокчейне и переводит на него лампорты для покрытия аренды.  
Она используется, когда нужно добавить новый счёт данных, принадлежащий программе.

#### Принцип работы  
- Плательщик (`from_pubkey`) создаёт новый аккаунт (`to_pubkey`) и переводит на него `lamports`.  
- Выделяется `space` байт под `data`.  
- Назначается владелец (`owner`) — программа, которая сможет работать с этим аккаунтом.  
- System Program сама вызывает внутри `allocate` и `assign`.

#### Пример  
Используем код из [`examples/Python/L8-SystemProgram_create_account.py`](../examples/Python/L8-SystemProgram_create_account.py):
```python
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import CreateAccountParams, create_account

payer = Keypair()
new_account = Keypair()
program_owner = Pubkey.from_string("11111111111111111111111111111111")  # System Program

ix = create_account(CreateAccountParams(
    from_pubkey=payer.pubkey(),
    to_pubkey=new_account.pubkey(),
    lamports=1_000_000,
    space=64,
    owner=program_owner
))

print(ix)
```

#### Когда используется  
- При инициализации PDA или data-аккаунта программы.  
- При создании вспомогательных структур (treasury, config и т.д.).  
- Внутри большинства on-chain программ Solana как первый шаг деплоя state.

#### Ограничения  
- Новый аккаунт должен быть свежим (не существовать в цепочке).  
- Плательщик обязан быть подписантом.  
- Необходимо рассчитать минимальный депозит для rent-exempt (см. Урок 26).  
- Нельзя создавать аккаунты с `space > 10 МБ`.

#### Связанные инструкции  
`create_account` выполняет комбинацию `allocate + assign + transfer`.

---

### 10.3. Выделение памяти (`allocate`)

Назначение: инструкция **`allocate`** резервирует память (`data`-поле) в уже существующем аккаунте.  
Используется, когда нужно задать или изменить размер данных без пересоздания аккаунта.

Как работает:  
- Меняет значение `account.data_len` на `space`.  
- Требует подпись владельца аккаунта.  
- Проверяет, что баланс позволяет оставаться rent-exempt.  
- Применяется только к не-executable аккаунтам.

Пример  
Используем код из [`examples/Python/L8-SystemProgram_allocate.py`](../examples/Python/L8-SystemProgram_allocate.py):
```python
from solders.pubkey import Pubkey
from solders.system_program import AllocateParams, allocate

account_pubkey = Pubkey.from_string("11111111111111111111111111111111")
ix = allocate(AllocateParams(pubkey=account_pubkey, space=128))
print(ix)
```

Когда используется:  
- При подготовке PDA-аккаунтов перед записью state.  
- Для реконфигурации или повторного использования существующих аккаунтов.  
- Внутри `create_account` (System Program вызывает `allocate` автоматически).

Ограничения:  
- Аккаунт должен быть подписантом.  
- Только владелец может выполнять `allocate`.  
- Расширение размера требует дополнительного депозита rent-exempt.  
- Нельзя применять к программам (`executable=True`).

Связанные инструкции:  
Обычно вызывается вместе с `assign`, если нужно назначить нового владельца после изменения памяти.

---

### 10.4. Назначение владельца (`assign`)

Назначение: инструкция **`assign`** меняет владельца (`owner`) существующего аккаунта.  
Используется, чтобы передать контроль над аккаунтом другой программе.

Как работает:  
- Меняет поле `owner` в структуре аккаунта.  
- Разрешено только текущему владельцу аккаунта.  
- После выполнения только новая программа может изменять данные аккаунта.

Пример  
Используем код из [`examples/Python/L8-SystemProgram_assign.py`](../examples/Python/L8-SystemProgram_assign.py):
```python
from solders.pubkey import Pubkey
from solders.system_program import AssignParams, assign

account_pubkey = Pubkey.from_string("11111111111111111111111111111111")
new_owner = Pubkey.from_string("11111111111111111111111111111111")

ix = assign(AssignParams(pubkey=account_pubkey, owner=new_owner))
print(ix)
```

Когда используется:  
- После `allocate`, когда аккаунт готов передать управление программе.  
- При миграции state-аккаунтов между версиями программы.  
- В системных сценариях `create_account` → `assign`.

Ограничения:  
- Аккаунт должен быть system-owned (владелец = System Program).  
- Текущий владелец должен подписать транзакцию.  
- Нельзя назначить владельцем `executable` аккаунт.

Связанные инструкции:  
Часто идёт последним шагом цепочки `create_account → allocate → assign`.

---

## 11. Типичные ошибки и как их избегать

| Ситуация | Причина | Решение |
|---|---|---|
| `TypeError: expected Pubkey` | Передан `str` вместо `Pubkey` | Всегда приводите к `Pubkey.from_string(...)` |
| `AccountNotFound` при отправке | У плательщика нет SOL | Сделайте `request_airdrop()` в Devnet; проверьте payer |
| `BlockhashNotFound` | Устаревший `recent_blockhash` | Обновите через `get_latest_blockhash()` и пересоберите `Message` |
| `Custom program error` | Неверные `AccountMeta`/порядок/данные | Проверьте порядок аккаунтов, `is_signer`, `is_writable`, формат `data` |
| `expected 64 bytes` для `Keypair.from_bytes` | Сохраняли только 32 байта секрета | Сохраняйте/загружайте 64 байта: `bytes(kp)` |

---

## 12. Практическое задание

1) Создайте `Keypair`, сохраните 64 байта в файл, восстановите из файла, убедитесь, что `pubkey()` совпадает.  
2) Постройте инструкцию `transfer` и сформируйте `Message` с актуальным блокхешем; сериализуйте `Transaction` в байты (не отправляйте).  
3) Попробуйте пометить аккаунт как `is_writable=False` там, где требуется запись — получите ошибку и объясните её причину.  
4) Используя `get_multiple_accounts`, считайте два системных аккаунта и сравните их поля `owner` и `executable`.

---

## 13. Ключевые выводы

- `solders` — это сердце типов Solana в Python: ключи, подписи, инструкции, транзакции.  
- Строгие типы сокращают класс ошибок «передал не то» и ускоряют разработку.  
- `solana` + `solders` = стандартный стек: первый говорит с сетью, второй гарантирует корректные байты.  
- Понимание `AccountMeta` и порядка аккаунтов критично для корректного исполнения программ.

---

## 14. Навигация

[← Урок 7 — Работа с библиотекой `solana` и RPC](Lesson_7.md)  
[→ Урок 9 — Генерация Keypair и форматы ключей (raw, hex, base58)](Lesson_9.md)

