# Урок 3. Подключение уже существующих кошельков (импорт и восстановление)

**Цель урока:** научиться безопасно подключать (импортировать) уже существующие кошельки: по мнемонике, по приватному ключу (Base58), или по JSON-файлу.

---

## 1) Когда нужно импортировать кошелёк?

- Восстановление доступа на новом компьютере.
- Работа с несколькими машинами/серверами.
- Перенос кошелька между приложениями (например, Phantom → локальный скрипт).

**ВАЖНО:** никогда не вставляйте мнемонику в публичные формы и не отправляйте её по мессенджерам без шифрования и острой на то необходимости.

---

## 2) Методы подключения (реализованы в `examples/Wallet.py`)
В данном уроке мы рассмотрим 3 метода подключения уже существующих кошельков. Если Вы не знаете, какой кошелек требуется для данного урока, предлагаем Вам изучить предыдущий урок: [`Создание кошелька в сети Solana`](../learning/lesson2.md)
- `mnemonic` — аргумент `value` — строка мнемоники (12 или 24 слова).
- `base58` — аргумент `value` — приватный ключ в base58 формате.
- `file` — аргумент `value` — путь к JSON файлу, содержащему `mnemonic` или `secret_key_base58`.

Пример сигнатуры (в `Wallet.py`):
```python
def load_wallet(method: str, value: str, network="devnet"):
    # method: "mnemonic" | "base58" | "file"
    pass
```

---

## 3) Практика: восстановление из `wallet.json`

### Шаг 1 — Убедитесь, что `wallet.json` у вас в безопасной папке.
### Шаг 2 — Подключаемся:
```bash
python -i
>>> from examples.Wallet import load_wallet
>>> kp = load_wallet("file", "wallet.json", network="devnet")
>>> print(kp.pubkey())
```
Ожидаемый вывод (пример):
```
Connected wallet (method type: file-mnemonic):
Public key: 542RNhK4ThyBDJWBnxpqqhZEzEuMtQ47DLiJAnxgowig
RPC: https://api.devnet.solana.com

Balance: 0 lamports = 0 SOL
```

### Восстановление по мнемонике напрямую:
```python
>>> load_wallet("mnemonic", "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12", network="devnet")
```

### Подключение по base58 (если у Вас имеется private-key base58):
```python
>>> load_wallet("base58", "23rR...Br", network="devnet")
```

---

## 4) Советы по безопасности при импорте

- Используй временное окружение (виртуальная машина или новая виртуальная среда) при импортировании чужих/подозрительных библиотек.
- Проверяй адрес сразу после импорта — он должен совпадать с адресом в оригинальном кошельке (Phantom/CLI).
- Не держи мнемонику в переменной окружения без защиты — при утечке CI/CD токенов приватность будет скомпрометирована.

---

## 5) Проверка баланса и состояния

После импорта советуем всегда проверять баланс аккаунта.
Пример с использованием предыдущих уроков:
```python
from examples.Wallet import load_wallet
from examples.Connect import get_connection
kp = load_wallet("file", "wallet.json", network="devnet")
client = get_connection("devnet")
print(client.get_balance(kp.pubkey()).value / 1_000_000_000, "SOL")
```
Ожидаемый вывод (пример):
```
Connected wallet (method type: file-mnemonic):
Public key: GsErFFTCxBqT6HWUgdzAd3e9zLBvKicw7ENdoc3pZJM8

Connected to Solana cluster (devnet): GetVersionResp(RpcVersionInfo(2.3.6))

0.0 SOL

```
---
✅ Получив вывод, схожий с тем, что указан в примере - Поздравляем, Вы успешно подключили существующий кошелек к сети Solana!

[`Предыдущий урок`](../learning/lesson2.md) | [`Следующий урок`](../learning/lesson4.md)
