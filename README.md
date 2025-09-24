
# Solana Wallet Tutorial

Учебный проект на Python для работы с кошельками в сети **Solana**  
с использованием библиотек [`solders`](https://pypi.org/project/solders/) и [`bip_utils`](https://pypi.org/project/bip-utils/).

Проект позволяет:
- Создавать кошельки Solana (12 или 24 слова).
- Сохранять данные кошелька в файл.
- Подключаться к кошельку по:
  - Мнемонической фразе
  - Base58 приватному ключу
  - JSON-файлу
- Получать баланс кошелька в SOL.

---

## 📦 Установка

1. Клонируем репозиторий:
```bash
git clone https://github.com/Stanislav1710/solana-tutorial.git
cd solana-tutorial
```

2. Создаём виртуальное окружение и устанавливаем зависимости:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

---

## 🛠 Как использовать

### 1. Создать кошелёк
```python
from wallet import create_wallet

# Создаёт кошелёк с 12 словами и сохраняет в wallet.json
create_wallet(save_to_file=True, filename="wallet.json", words_number=12)
```

### 2. Подключиться к кошельку

#### По мнемонике:
```python
from wallet import load_wallet

load_wallet("mnemonic", "ваша мнемоническая фраза", network="devnet")
```

#### По приватному ключу (Base58):
```python
load_wallet("base58", "ваш приватный ключ в base58", network="mainnet")
```

#### Через файл:
```python
load_wallet("file", "wallet.json", network="devnet")
```

---

## ⚙️ Поддерживаемые сети
- **Devnet**: `https://api.devnet.solana.com`  
- **Mainnet**: `https://api.mainnet-beta.solana.com`  

---

## 📂 Структура проекта
```
solana-tutorial/
│
├── wallet.py        # Основной код проекта
├── requirements.txt # Зависимости
├── README.md        # Эта документация
└── .gitignore       # Файлы, исключённые из git
```

---

## 🔐 Безопасность
- Никогда не публикуйте приватные ключи и мнемонические фразы.  
- Используйте `.gitignore` для исключения файлов с приватными данными.  

---

## 📜 Лицензия
MIT License © Stanislav1710
