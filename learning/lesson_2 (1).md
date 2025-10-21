# Урок 2 — Основные сущности: аккаунты, программы, транзакции, инструкции

---

## 5. Транзакция (Transaction)

### 5.1. Что такое транзакция

**Транзакция (Transaction)** — это контейнер, в котором собраны одна или несколько инструкций.  
Она определяет последовательность действий и подтверждает права на выполнение этих действий с помощью цифровых подписей.

---

### 5.2. Как формируется транзакция

1. Создаётся инструкция (`Instruction`) — описание действия.
2. Инструкция добавляется в сообщение (`Message`).
3. Транзакция создаётся и подписывается ключами отправителей.
4. Транзакция отправляется на RPC-узел для выполнения.

---

### 5.3. Пример: создание и отправка транзакции (актуально для `solana==0.36.9`, `solders==0.26.0`)

```python
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.system_program import TransferParams, transfer
from solders.transaction import Transaction
from solders.message import Message
from solana.rpc.api import Client

client = Client("https://api.devnet.solana.com")

sender_kp = Keypair()
recipient = Pubkey.from_string("11111111111111111111111111111111")

ix = transfer(
    TransferParams(
        from_pubkey=sender_kp.pubkey(),
        to_pubkey=recipient,
        lamports=1000
    )
)

recent_blockhash = client.get_latest_blockhash().value.blockhash

message = Message.new_with_blockhash(
    [ix],
    sender_kp.pubkey(),
    recent_blockhash
)

# Создаём транзакцию, подписываем и отправляем
tx = Transaction([sender_kp], message, recent_blockhash)
tx.partial_sign([sender_kp], recent_blockhash)
resp = client.send_transaction(tx)

print(resp)
```

---

### 5.4. Пример реального вывода

```
SendTransactionResp {
  result: "3hP6dy5cZyTz7e3fthE4bsX76z4p3PrK4m2Pn4dp9o8bJ5hYbDkPj7ZdbSknEjB6mPqsxX1WbnMExbHd9aSuiTrL",
  context: RpcResponseContext { slot: 416135991 }
}
```

---

### 5.5. Что происходит «под капотом»

| Этап | Что выполняется | Объект |
|------|------------------|--------|
| 1 | Создаётся инструкция `transfer()` | `Instruction` |
| 2 | Инструкция добавляется в сообщение | `Message.new_with_blockhash()` |
| 3 | Транзакция создаётся и подписывается | `Transaction` + `partial_sign()` |
| 4 | RPC-узел проверяет подписи и передаёт транзакцию в сеть | `Client.send_transaction()` |
| 5 | Валидаторы выполняют действия | Solana runtime |

---

### 5.6. Что важно знать

- Одна транзакция может содержать несколько инструкций.  
- Подписи подтверждают права на изменение указанных аккаунтов.  
- Узлы отклоняют транзакции с неверными или неполными подписями.  

---

### 5.7. Проверка транзакции без отправки в сеть

Если у вас нет средств на счёте или вы хотите протестировать код без отправки транзакции, можно использовать **эмуляцию (симуляцию)**.

```python
simulation = client.simulate_transaction(tx)
print(simulation)
```

**Что делает:**  
Эта функция запускает транзакцию в тестовом режиме и проверяет, будет ли она выполнена успешно, не записывая результат в блокчейн.

**Когда использовать:**  
- Нет средств на счёте отправителя.  
- Нужно убедиться, что инструкция корректна.  
- При отладке новых программ.

---

## 6. Навигация

[← Урок 1 — Что такое Solana и почему она особенная](Lesson_1.md)  
[→ Урок 3 — Ключи и безопасность](Lesson_3.md)

