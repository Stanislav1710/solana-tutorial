# Урок 14 — Перевод SOL: собрать, подписать, отправить и получить подтверждение

---

## 1. Введение

В предыдущем уроке мы научились получать тестовые SOL в сети **Devnet** (Урок 13), а ранее — подписывать транзакции (Урок 11).
Теперь мы выполним полноценный перевод SOL через RPC:

1. загрузим учебный кошелёк `course_wallet.bin` (Урок 10);
2. соберём инструкцию перевода (`System Program → transfer`, см. Урок 8);
3. сформируем сообщение (`Message`), подпишем транзакцию (`Transaction`);
4. отправим транзакцию в Devnet;
5. дождёмся подтверждения выполнения.

В этом уроке мы выполняем **перевод самому себе**.
Это упрощает структуру урока: транзакция настоящая, но средства остаются на том же адресе.

---

## 2. Как работает перевод SOL

Перевод SOL в Solana выполняется программой **System Program**.
Она получает инструкцию:

* от кого отправлять средства (отправитель должен подписать транзакцию);
* кому переводить (в нашем случае — тому же адресу);
* сколько лампортов списать и зачислить.

Важно:

* 1 SOL = 1 000 000 000 lamports;
* отправитель обязан оплатить комиссию за транзакцию;
* даже если перевод самому себе, плательщик должен иметь баланс.

---

## 3. Минимальный рабочий пример (Python)

В примере ниже мы:

1. загружаем `course_wallet.bin`;
2. подключаемся к Devnet;
3. проверяем баланс;
4. создаём инструкцию перевода `transfer`;
5. собираем `Message`, подписываем транзакцию;
6. отправляем её через RPC и выводим сигнатуру;
7. дополнительно — запрашиваем статус выполнения (commitment).

Используем код из [`examples/Python/L14-Send_SOL.py`](../examples/Python/L14-Send_SOL.py):

```python
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.transaction import Transaction

# RPC Devnet
DEVNET = "https://api.devnet.solana.com"
client = Client(DEVNET)

# 1. Загружаем учебный кошелёк (создан в Уроке 10)
with open("course_wallet.bin", "rb") as f:
    wallet = Keypair.from_bytes(f.read())

pubkey = wallet.pubkey()
print("Адрес:", pubkey)

# 2. Проверяем баланс перед отправкой
before = client.get_balance(pubkey).value
print("Баланс до:", before, "lamports")

# 3. Готовим инструкцию перевода самому себе
ix = transfer(TransferParams(
    from_pubkey=pubkey,
    to_pubkey=pubkey,
    lamports=1  # перевод 1 лампорта
))

# 4. Получаем актуальный blockhash
latest = client.get_latest_blockhash().value
blockhash = latest.blockhash

# 5. Собираем Message
msg = Message.new_with_blockhash([ix], pubkey, blockhash)

# 6. Формируем и подписываем Transaction
tx = Transaction([wallet], msg, blockhash)
tx.partial_sign([wallet], blockhash)

# 7. Отправляем транзакцию в сеть
resp = client.send_transaction(tx)
sig = resp.value
print("Сигнатура транзакции:", sig)

# 8. Проверяем статус выполнения
status = client.get_signature_statuses([sig]).value[0]
print("Статус выполнения:", status)

# 9. Баланс после отправки
after = client.get_balance(pubkey).value
print("Баланс после:", after, "lamports")
```

---

## 4. Разбор кода и используемых структур

### 4.1. Инструкция `transfer`

Мы вызываем:

```python
ix = transfer(TransferParams(...))
```

Эта инструкция:

* указывает отправителя (`from_pubkey`);
* указывает получателя (`to_pubkey`);
* задаёт количество лампортов (`lamports`);
* автоматически формирует правильный список `AccountMeta`.

См. Урок 8 — System Program.

---

### 4.2. Что мы подписываем

Подписывается объект `Message`:

```python
msg = Message.new_with_blockhash([ix], pubkey, blockhash)
```

В `Message` входят:

* инструкции;
* упорядоченный список всех аккаунтов;
* адрес плательщика комиссии (payer);
* актуальный blockhash (см. Урок 11).

---

### 4.3. Формирование транзакции

```python
tx = Transaction([wallet], msg, blockhash)
tx.partial_sign([wallet], blockhash)
```

Подписывать обязан:

* плательщик комиссии (payer);
* автор действий по переводу (тот же аккаунт).

Если подписи не хватает → ошибка `missing required signature`.

---

### 4.4. Отправка транзакции

```python
resp = client.send_transaction(tx)
sig = resp.value
```

RPC возвращает **сигнатуру транзакции**.
Это строка, по которой можно проверить статус выполнения.

---

### 4.5. Проверка результата

```python
status = client.get_signature_statuses([sig]).value[0]
```

Статус может содержать:

* `slot` — в каком блоке выполнена;
* `confirmations` — количество подтверждений;
* `err` — ошибка выполнения (если была);
* `confirmation_status` — `processed`, `confirmed`, `finalized` (см. Урок 15).

---

## 5. Схема процесса отправки транзакции

```
[Instruction (transfer)]
           │
           ▼
     [ Message ]
           │
           ▼
  [ Transaction + подписи ]
           │
           ▼
  RPC send_transaction()
           │
           ▼
   Сигнатура (Signature)
           │
           ▼
  get_signature_statuses()
```

---

## 6. Частые ошибки и их причины

| Сообщение                    | Причина                                    | Решение                                                                     |
| ---------------------------- | ------------------------------------------ | --------------------------------------------------------------------------- |
| `AccountNotFound`            | На кошельке нет SOL                        | Пополнить через airdrop (Урок 13)                                           |
| `missing required signature` | Транзакция не подписана кошельком          | Проверить `partial_sign()`                                                  |
| `BlockhashNotFound`          | Blockhash устарел                          | Запросить новый blockhash                                                   |
| `ReadonlyLamportChange`      | Попытка изменить баланс read-only аккаунта | Проверить `is_writable` создаётся автоматически — не модифицировать вручную |

---

## 7. Практические задания

1. Измени код и выполни перевод 10 лампортов.
2. Выведи разницу баланса `after - before`.
3. Поставь `lamports=0` — проверь, какая комиссия будет списана.
4. Создай цикл и отправь 3 транзакции подряд, записав все сигнатуры в список.
5. Для каждой сигнатуры выведи уровень подтверждения (`confirmation_status`).

---

## 8. Ключевые выводы

* Любой перевод SOL — это инструкция `System Program → transfer`.
* Для выполнения транзакции нужно: `Instruction → Message → Transaction → подпись → отправка`.
* Отправитель должен подписывать транзакцию и оплачивать комиссию.
* Перевод самому себе — удобный тестовый пример, который отрабатывает весь путь транзакции.
* Проверка статуса (`get_signature_statuses`) позволяет убедиться в подтверждении транзакции.
* Комиссии и уровни подтверждения подробно рассматриваются в следующем уроке (Урок 15).

---

## Навигация

[← Урок 13 — Airdrop в devnet и проверка баланса](Lesson_13.md)  
[→ Урок 15 — Commitment levels: processed / confirmed / finalized](Lesson_15.md)


