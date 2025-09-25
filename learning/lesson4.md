# Урок 4. Учимся создавать транзакции для отправки SOL — подробный гид

**Цель урока:** понять, что такое транзакция в Solana, как формируется, подписывается и отправляется. Практика будет использовать [`examples/Transaction.py`](../examples/Transaction.py).

До этого момента мы:  
- разобрались с принципами работы Solana,  
- научились создавать и подключать кошельки,
- смотреть баланс SOL подключенных кошельков.

Теперь пришло время сделать первый перевод токенов **SOL** с одного кошелька на другой.  

---

## 🔑 Ключевые принципы транзакций в Solana

1. **Blockhash** — это «свежая метка времени» для транзакции. Без неё транзакция не будет принята сетью.  
2. **Инструкция (Instruction)** — команда, которую выполняет сеть. В нашем случае это перевод SOL с одного кошелька на другой.  
3. **Message** — упакованный набор инструкций + информация об отправителе.  
4. **Transaction** — подписанное сообщение, которое можно отправить в блокчейн.  

---

## ⚙️ Код отправки SOL  

Файл для ознакомления: [`Transaction.py`](../examples/Transaction.py)  

---

## 🛠️ Практика (devnet)

1. Открой файл `Transaction.py`.
2. Подключите уже существующий кошелек Solana в **wallet**
3. Укажи **адрес получателя** вместо `"recipient_address"`.  
4. Убедись, что у отправителя есть немного SOL на **Devnet** (можно получить в [Solana Faucet](https://faucet.solana.com/)).  
5. Запусти файл:  

```bash
python Transaction.py
```

5. Пример вывода:
```
Connected wallet (method type: file-mnemonic):
Public key: GsErF.....w7ENdoc3pZJM8
RPC: https://api.devnet.solana.com 

Balance: 1000000000 lamports = 1.0 SOL
Connected to Solana cluster (devnet): GetVersionResp(RpcVersionInfo(3.0.2))
✅ Transaction sent! TxID: 4FRi6Xcfa1z3.....gqxJtRuZJvW
```

В консоли ты увидишь `TxID`.  
Скопируй его и проверь транзакцию в [Solana Explorer Devnet](https://explorer.solana.com/?cluster=devnet) для сети "devnet" или [Solana Explorer Mainnet Beta](https://explorer.solana.com/) для сети "mainnet".  

---

## 🎯 Результат

Ты научился:  
✅ Создавать инструкцию для перевода SOL  
✅ Упаковывать её в транзакцию  
✅ Подписывать транзакцию приватным ключом  
✅ Отправлять её в сеть и отслеживать результат  


[`Предыдущий урок`](../learning/lesson3.md) | [`Следующий урок`](../learning/lesson5.md)
