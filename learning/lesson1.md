# 📘 Lesson 1: Основы работы с Solana

## 🔹 Теория

**Что такое Solana?**
Solana — это высокопроизводительная блокчейн-сеть, созданная для масштабируемых приложений.  
Её ключевые преимущества:

- ⚡ **Высокая скорость транзакций** — до 65 000 операций в секунду.  
- 💰 **Низкие комиссии** — транзакции стоят доли цента.  
- 🔒 **Proof of History (PoH)** — уникальный алгоритм синхронизации времени, повышающий безопасность и скорость.  
- 🌍 **Развитая экосистема** — DeFi, NFT, GameFi и многое другое.  

---

## 🔹 Практика

### 1. Установка Python и IDE

1. Скачайте Python с [официального сайта](https://www.python.org/downloads/).  
2. Проверьте установку в терминале:

```bash
python --version
```

3. Установите удобную IDE: **VS Code** или **PyCharm**.

---

### 2. Создание виртуальной среды

В папке проекта выполните:

```bash
python -m venv .venv
```

Активация окружения:
- Windows:
  ```bash
  .venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source .venv/bin/activate
  ```

---

### 3. Установка зависимостей

В проекте есть файл `requirements.txt`. Установите все зависимости:

```bash
pip install -r requirements.txt
```

---

### 4. Подключение к Solana

Теперь можно подключиться к сети.  
Используем код из [`examples/Connect.py`](../examples/Connect.py) или скопируйте его ниже:

```python
from solana.rpc.api import Client

def get_connection(network="devnet"):
    endpoints = {
        "devnet": "https://api.devnet.solana.com",
        "mainnet": "https://api.mainnet-beta.solana.com",
    }
    client = Client(endpoints[network])
    print(f"Connected to {network}: {client.get_version()}")
    return client

if __name__ == "__main__":
    get_connection("devnet")
```

📌 Этот код проверит соединение с Devnet и выведет версию кластера.

**Пример успешного выполнения:**
```bash
Connected to Solana cluster (devnet): GetVersionResp(RpcVersionInfo(2.3.6))
```



---

✅ Поздравляем, Вы успешно подключились к Solana!

[`Следующий урок`](../learning/lesson2.md)

