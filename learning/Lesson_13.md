# Урок 13 — Airdrop в devnet и проверка баланса через RPC

---

## 1. Введение

В этом уроке мы впервые «кормим» наш учебный кошелёк `course_wallet` настоящими тестовыми монетами в сети **Devnet**.

Ты уже знаешь:

* что такое ключи и `Keypair` (Урок 9);
* как мы создали и храним `course_wallet.bin` (Урок 10);
* как устроены подписи (Урок 11);
* как безопасно хранить ключи (Урок 12).

Теперь нам нужно:

1. Загрузить `course_wallet` из файла `course_wallet.bin`.
2. Подключиться к **Devnet** через `solana.rpc.api.Client`.
3. Запросить airdrop (получить тестовый SOL).
4. Проверить баланс до и после операции.

> Во всех следующих уроках (переводы SOL, работа с токенами и т.д.) мы **используем один и тот же** `course_wallet.bin` как основной учебный кошелёк.

---

## 2. Что такое airdrop и зачем он нужен в Devnet

**Airdrop** — это бесплатная выдача тестовых монет (SOL) в учебной сети Devnet.

Важно:

* В **Devnet** SOL **не имеют реальной стоимости**.
* Airdrop создан для разработчиков, чтобы они могли:

  * тестировать переводы;
  * вызывать программы;
  * оплачивать комиссии без настоящих денег.

В **Mainnet**:

* airdrop **отсутствует**;
* каждая монета SOL имеет рыночную стоимость;
* пополнение делается через биржи, обменники, мосты и т.п.

---

## 3. Lamports и SOL

Внутри сети Solana баланс хранится в **лампортах** (lamports).

* 1 SOL = 1_000_000_000 lamports (10⁹ лампортов).
* Лампорты — это минимальная единица, как «копейка» для рубля или «цент» для евро.

В коде мы:

* храним баланс и работаем с числами в lamports (целые числа);
* при выводе можем перевести значение в SOL, разделив на `1_000_000_000`.

---

## 4. Общая схема работы airdrop через Python

Последовательность действий:

1. Подключиться к RPC Devnet:

   * URL: `https://api.devnet.solana.com`
2. Загрузить `Keypair` из файла `course_wallet.bin`.
3. Получить публичный ключ (`pubkey`) кошелька.
4. Узнать текущий баланс (`get_balance`).
5. Вызвать `request_airdrop(pubkey, amount_lamports)`.
6. Немного подождать и ещё раз вызвать `get_balance`.
7. Убедиться, что баланс увеличился.

---

## 5. Минимальный пример (Python)

В этом примере мы:

* загружаем учебный кошелёк `course_wallet.bin`;
* запрашиваем **1 SOL** через airdrop в Devnet;
* выводим баланс до и после.

Используем код из [`examples/Python/L13-Airdrop_and_balance.py`](../examples/Python/L13-Airdrop_and_balance.py):

```python
from solana.rpc.api import Client
from solders.keypair import Keypair

# Адрес RPC Devnet
DEVNET_RPC = "https://api.devnet.solana.com"

# Константы для пересчёта
LAMPORTS_PER_SOL = 1_000_000_000
AIRDROP_SOL = 1.0  # сколько SOL запросить

# 1. Подключаемся к Devnet
client = Client(DEVNET_RPC)

# 2. Загружаем учебный кошелёк из course_wallet.bin (см. Урок 10)
with open("course_wallet.bin", "rb") as f:
    wallet_bytes = f.read()

wallet = Keypair.from_bytes(wallet_bytes)
pubkey = wallet.pubkey()
print("Адрес course_wallet:", pubkey)

# 3. Проверяем баланс до airdrop
before_resp = client.get_balance(pubkey)
before_lamports = before_resp.value
print("Баланс до airdrop:", before_lamports, "lamports")

# 4. Запрашиваем airdrop (1 SOL)
amount_lamports = int(AIRDROP_SOL * LAMPORTS_PER_SOL)
airdrop_resp = client.request_airdrop(pubkey, amount_lamports)
sig = airdrop_resp.value
print("Сигнатура airdrop:", sig)

# 5. Повторно проверяем баланс
after_resp = client.get_balance(pubkey)
after_lamports = after_resp.value
print("Баланс после airdrop:", after_lamports, "lamports")

# 6. Для удобства выводим в SOL
print("Баланс в SOL до:", before_lamports / LAMPORTS_PER_SOL)
print("Баланс в SOL после:", after_lamports / LAMPORTS_PER_SOL)
```

Обрати внимание:

* Мы **не** используем `["result"]["value"]`, а берём баланс через `.value`.
  Методы `get_balance` и `request_airdrop` возвращают объекты-ответы (`GetBalanceResp`, `RequestAirdropResp`), у которых основное поле находится в свойстве `.value`.
* В коде только самые необходимые переменные:

  * `DEVNET_RPC`, `LAMPORTS_PER_SOL`, `AIRDROP_SOL` — для наглядности;
  * `wallet`, `pubkey`, `before_lamports`, `after_lamports`.

---

## 6. Разбор методов: `get_balance` и `request_airdrop`

### 6.1. `get_balance(pubkey)`

**Назначение:** получить баланс аккаунта в lamports.

Краткий вид (как мы используем):

```python
resp = client.get_balance(pubkey)
lamports = resp.value
```

Основные параметры:

| Параметр | Тип      | Обязательный | Описание                                |
| -------- | -------- | ------------ | --------------------------------------- |
| `pubkey` | `Pubkey` | Да           | Адрес аккаунта, баланс которого читаем. |

Что возвращает (упрощённо):

* объект ответа `GetBalanceResp`;
* основное поле — `resp.value` (целое число lamports).

---

### 6.2. `request_airdrop(pubkey, lamports)`

**Назначение:** запросить тестовые SOL в Devnet для указанного аккаунта.

Краткий вид:

```python
resp = client.request_airdrop(pubkey, amount_lamports)
sig = resp.value
```

Параметры:

| Параметр   | Тип      | Обязательный | Описание                                  |
| ---------- | -------- | ------------ | ----------------------------------------- |
| `pubkey`   | `Pubkey` | Да           | Адрес получателя airdrop.                 |
| `lamports` | `int`    | Да           | Сколько lamports запросить (целое число). |

Что возвращает:

* объект `RequestAirdropResp`;
* `resp.value` — это `Signature` транзакции airdrop.

---

## 7. Порядок действий в Devnet (короткая инструкция)

1. Убедись, что у тебя есть файл `course_wallet.bin` (Урок 10).
2. Убедись, что он **не** в git (добавлен в `.gitignore`, Урок 12).
3. Запусти скрипт `L13-Airdrop_and_balance.py`.
4. Проверь вывод:

   * адрес `course_wallet`;
   * баланс до airdrop (часто 0);
   * сигнатуру airdrop;
   * баланс после airdrop (должен увеличиться на запрошенный объём);
   * значения в SOL.

Если баланс не меняется:

* возможно, RPC Devnet временно перегружен;
* возможно, для этого адреса достигнут лимит airdrop;
* попробуй повторить запрос через некоторое время или уменьшить `AIRDROP_SOL`.

---

## 8. Типичные ошибки и как их распознать

| Симптом / сообщение                                       | Возможная причина                               | Что проверить                                   |
| --------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- |
| `TypeError: 'GetBalanceResp' object is not subscriptable` | Обращение к ответу как к словарю (`["result"]`) | Используй `.value`, как в примере урока.        |
| Баланс остаётся 0 после airdrop                           | Airdrop не прошёл или лимит исчерпан            | Проверь лимиты, повтори запрос позже.           |
| Ошибка соединения с RPC                                   | Проблемы с сетью или RPC Devnet                 | Проверь интернет, URL `DEVNET_RPC`.             |
| Неправильный путь к `course_wallet.bin`                   | Файл отсутствует или лежит в другом каталоге    | Убедись, что скрипт запускается из корня курса. |

---

## 9. Практические задания

1. Измени `AIRDROP_SOL` на `0.1` и убедись, что баланс увеличивается именно на 0.1 SOL (в пересчёте на lamports).
2. Добавь простую проверку: если баланс уже больше 2 SOL, не запрашивай новый airdrop.
3. Выведи разницу баланса в SOL до и после операции, как отдельную строку.
4. Попробуй запустить скрипт несколько раз подряд и посмотри, изменится ли поведение RPC (лимиты Devnet).

---

## 10. Ключевые выводы

1. Airdrop в Devnet — это способ **бесплатно** получить тестовые SOL для обучения и разработки.
2. В этом курсе мы используем **единый кошелёк** `course_wallet.bin`, созданный в Уроке 10.
3. Баланс в Solana хранится в **lamports**, 1 SOL = 1_000_000_000 lamports.
4. Для получения средств через Python достаточно двух основных вызовов:

   * `get_balance(pubkey)` → `resp.value`;
   * `request_airdrop(pubkey, lamports)` → `resp.value` (Signature).
5. Мы не используем CLI в этом уроке — всё делаем через `solana` и `solders` в минималистичном Python-коде.

---

## Навигация

[← Урок 12 — Безопасное хранение ключей](Lesson_12.md)  
[→ Урок 14 — Перевод SOL: собрать, подписать, отправить, дождаться подтверждения](Lesson_14.md)
