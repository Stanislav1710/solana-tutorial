# Урок 11 — Подписи транзакций: как и почему подписываем

---

## 1. Введение

Подпись в Solana доказывает право выполнять действие от имени аккаунта и защищает транзакцию от подмены.  
Подписывается **сообщение (Message)**, в котором перечислены инструкции, плательщик комиссии (payer) и `recent_blockhash`.  
Именно подпись делает транзакцию допустимой для выполнения валидаторами.

Связанные уроки: Урок 7 (RPC/commitment), Урок 8 (структуры `solders`), Урок 9 (Keypair/Ed25519), Урок 10 (единый `course_wallet`), Урок 14 (перевод SOL).

---

## 2. Что именно подписывается

Подписывается **Message**, а не «сырые инструкции». В `Message` входят:
- упорядоченный список `Instruction`;
- список всех упомянутых в инструкциях аккаунтов с флагами прав (включая payer);
- поле `recent_blockhash` (защита от повторной отправки и устаревания).

Только после подписи на основе `Message` формируется `Transaction`.

---

## 3. Кто обязан подписывать

- Все аккаунты, отмеченные в инструкциях как `is_signer=True`.
- Плательщик комиссии (payer) **всегда** должен подписать транзакцию.
- Программы (program id) **не** подписывают — они исполняются детерминированно.

Нельзя менять данные/баланс аккаунта, если он не присутствует в `accounts` и не имеет корректных прав. См. Урок 2 (сущности) и Урок 8 (AccountMeta).

---

## 4. Как работает подпись (в контексте Ed25519)

1) Из `Message` формируется каноничное бинарное представление.  
2) Вычисляется хэш (внутренне, согласно протоколу).  
3) Подписант (Ed25519) вычисляет подпись над этим хэшом с использованием приватного ключа.  
4) Валидатор проверяет подпись по публичному ключу аккаунта.

Важно: Любое изменение `Message` (даже порядка аккаунтов) делает подпись недействительной.

---

## 5. Загрузка `course_wallet` и локальная подпись минимальной транзакции

В этом курсе мы используем единый ключ из Урока 10: `course_wallet.bin`. Если не создали и не пополнили — выполните Урок 10 и пополните баланс по Уроку 13.

Используем код из [`examples/Python/L11-Sign_minimal_tx.py`](../examples/Python/L11-Sign_minimal_tx.py):
```python
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.transaction import Transaction
from solana.rpc.api import Client

# 1) Грузим payer из course_wallet.bin
with open("course_wallet.bin", "rb") as f:
    raw = f.read()
payer = Keypair.from_bytes(raw)

client = Client("https://api.devnet.solana.com")

# 2) Формируем инструкцию (демонстрационно на самого себя)
ix = transfer(TransferParams(
    from_pubkey=payer.pubkey(),
    to_pubkey=payer.pubkey(),
    lamports=1
))

# 3) Актуальный blockhash и Message
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], payer.pubkey(), rbh)

# 4) Формируем Transaction и подписываем
tx = Transaction([payer], msg, rbh)
tx.partial_sign([payer], rbh)

print("Размер сериализованной транзакции, байт:", len(bytes(tx)))
# Отправку не выполняем в этом уроке
```

Примечание: если вы решите отправить транзакцию, убедитесь, что кошелёк пополнен (Урок 13), иначе получите `AccountNotFound`.

---

## 6. Получение подписи и анализ

Подписи хранятся внутри `Transaction`. Для целей аудита храните tx как bytes и сигнатуры отдельно. Сама «сигнатура транзакции», выдаваемая RPC при отправке — это результат `send_transaction`, см. Урок 8 (Signature) и Урок 14.

Используем код из [`examples/Python/L11-Inspect_signatures.py`](../examples/Python/L11-Inspect_signatures.py):
```python
from solders.keypair import Keypair
from solders.message import Message
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solana.rpc.api import Client

with open("course_wallet.bin", "rb") as f:
    payer = Keypair.from_bytes(f.read())

client = Client("https://api.devnet.solana.com")
ix = transfer(TransferParams(from_pubkey=payer.pubkey(), to_pubkey=payer.pubkey(), lamports=1))
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix], payer.pubkey(), rbh)

# Подписываем
tx = Transaction([payer], msg, rbh)
tx.partial_sign([payer], rbh)

# Сериализованные байты транзакции
raw = bytes(tx)
print("Первые 16 байт:", raw[:16].hex())
# В актуальных версиях структуры сигнатур доступны внутри tx; для совместимости выводим размер raw
print("Длина raw:", len(raw))
```

---

## 7. Частичная подпись (partial signing) и мульти‑подпись

`partial_sign([kp])` позволяет добавлять подписи по мере готовности сторон. Сценарии:
- оффлайн‑подписание: один участник формирует `Message`, подписывает, передаёт другому;
- многосторонние операции: каждый добавляет свою подпись перед отправкой.

Важно: транзакция будет принята сетью только если присутствуют **все обязательные подписи** (все аккаунты с `is_signer=True` + payer).

Используем код из [`examples/Python/L11-Partial_sign_demo.py`](../examples/Python/L11-Partial_sign_demo.py):
```python
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import AccountMeta, Instruction
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.transaction import Transaction
from solana.rpc.api import Client

# 1) Загружаем payer из course_wallet.bin (Урок 10)
with open("course_wallet.bin", "rb") as f:
    payer = Keypair.from_bytes(f.read())

client = Client("https://api.devnet.solana.com")

# 2) Второй обязательный подписант (демонстрационный ключ)
co_signer = Keypair()

# 3) Боевая инструкция (перевод 1 лампорта самому себе — просто для структуры)
ix_transfer = transfer(TransferParams(
    from_pubkey=payer.pubkey(),
    to_pubkey=payer.pubkey(),
    lamports=1
))

# 4) Манекен-инструкция, которая требует подпись co_signer
system_program_id = Pubkey.from_string("11111111111111111111111111111111")
ix_require_cosigner = Instruction(
    program_id=system_program_id,
    accounts=[AccountMeta(pubkey=co_signer.pubkey(), is_signer=True, is_writable=False)],
    data=b""  # пустые данные; мы не отправляем транзакцию
)

# 5) Сборка Message (оба подписанта обязательны)
rbh = client.get_latest_blockhash().value.blockhash
msg = Message.new_with_blockhash([ix_transfer, ix_require_cosigner], payer.pubkey(), rbh)

# 6) ВАЖНО: Конструктору Transaction нужно отдать ВСЕ обязательные ключи,
# иначе упадём с NotEnoughSigners
tx = Transaction([payer, co_signer], msg, rbh)

# Технически подпись выполняется в конструкторе. partial_sign можно вызывать повторно,
# но он уже ничего не добавит — обязательные подписи проставлены.
# Покажем вызов для иллюстрации API:
tx.partial_sign([payer, co_signer], rbh)

print("OK: транзакция собрана и подписана двумя ключами.")
print("Сериализованный размер:", len(bytes(tx)))


```

Для реальных многосторонних сценариев используйте инструкции программ, которые **реально** требуют вторую подпись (например, мультисиг‑кошельки, DAO‑схемы; см. Урок 55).

---

## 8. Типичные ошибки и диагностика

| Ошибка | Причина | Что сделать |
|---|---|---|
| `missing required signature` | Не все `is_signer` подписали | Проверьте список AccountMeta, подпишите всеми обязательными ключами |
| `BlockhashNotFound` | Устарел `recent_blockhash` | Запросите новый `get_latest_blockhash()` и пересоберите `Message` |
| `AccountNotFound` | Нулевой баланс плательщика | Пополните кошелёк (Урок 13) или используйте локальный validator |
| `ReadonlyLamportChange` | Пытаетесь менять read‑only аккаунт | Убедитесь, что целевой аккаунт `is_writable=True` и у программы есть права |

См. также: Урок 7 (commitment, RPC), Урок 8 (AccountMeta/Instruction), Урок 13 (airdrop), Урок 14 (отправка и подтверждение).

---

## 9. Практические задания

1) Подпишите транзакцию переводом 1 лампорт на самого себя, не отправляя её. Сохраните сериализованные байты в `tx.bin`.  
2) Добавьте вторую подпись (второй `Keypair`) и сравните сериализованный размер. Объясните разницу.  
3) Попробуйте изменить порядок аккаунтов в `Message` и заново подписать — сравните байты. Объясните, почему подпись изменилась.

---

## 10. Ключевые выводы

- Подписывается **Message**, включающий инструкции, порядок аккаунтов и `recent_blockhash`.
- Отправка возможна только при наличии всех обязательных подписей.
- `partial_sign` позволяет строить многосторонние процессы подписания.
- Для отправки убедитесь, что payer имеет баланс (Урок 13), и используйте Урок 14 как продолжение.

---

## Навигация

[← Урок 10 — Seed: бинарный seed, импорт и восстановление](Lesson_10.md)  
[→ Урок 12 — Безопасное хранение ключей](Lesson_12.md)

