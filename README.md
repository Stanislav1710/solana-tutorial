
---

<p align="center">
  <a href="https://solana.com">
    <img alt="Solana Developer Course" src="https://i.imgur.com/IKyzQ6T.png" width="500" />
  </a>
</p>

<p align="center">
    <a href="https://www.python.org/downloads/">
        <img src="https://img.shields.io/badge/python-3.11_|_3.12_|_3.13-blue">
    </a>
    <a href="https://pypi.org/project/solana/">
        <img src="https://img.shields.io/badge/solana-0.36.9-success">
    </a>
    <a href="https://pypi.org/project/solders/">
        <img src="https://img.shields.io/badge/solders-0.26.0-success">
    </a>
</p>

<p align="center">
    <a href="">
        <img src="https://img.shields.io/badge/Node.js-18_+-blue">
    </a>
    <a href="">
        <img src="https://img.shields.io/badge/@solana/web3.js-1.87.6_+-success">
    </a>
</p>
<p align="center">
    <a href="">
        <img src="https://img.shields.io/badge/TypeScript-5.0_+-blue">
    </a>
</p>

---

# Курс "Solana Developer"


Данный репозиторий содержит структурированную учебную программу, посвящённую разработке на Solana для Python, JavaScript и TypeScript разработчиков.

---

## Цель курса

Предоставить единое, понятное и практически ориентированное руководство по созданию и эксплуатации приложений, работающих в сети Solana:
от базового взаимодействия с сетью до проектирования масштабируемых и безопасных решений.

---

## Основная идея курса

Solana — это блокчейн-платформа для высокопроизводительных и масштабируемых приложений, где каждая транзакция подтверждается в считанные миллисекунды.  
Этот курс охватывает весь путь разработчика: от понимания базовых принципов сети до построения production-приложений и CI/CD инфраструктуры.

**В рамках программы рассматриваются:**

- структура сети Solana и принципы её работы;
- аккаунты, программы, инструкции, транзакции;
- взаимодействие с сетью через RPC и WebSocket;
- разработка и тестирование смарт-контрактов;
- использование библиотек `solana` и `solders` на Python;
- управление ключами, безопасное хранение и подписи;
- создание и обращение с токенами (SPL);
- архитектура dApp, off-chain индексация, кеширование и безопасность;
- разработка проектов для портфолио и подготовка к работе с open-source.

---

## Методика обучения

Каждый урок — это **самодостаточный блок**, включающий:
- теоретическое объяснение темы;
- минимальные примеры кода;
- краткую практику или задание;
- пояснение ключевых терминов;
- раздел *вопросов для самопроверки*.

Во всех примерах используется только необходимый минимум библиотек — **только `solana` и `solders`**, без избыточных зависимостей.  
Главная цель — понять принципы и структуру, а не просто воспроизвести код.

---

## Структура курса

Курс разделен на 19 тематических групп, каждая из которых содержит несколько уроков с постепенным увеличением сложности. Для быстрого перехода к конкретной теме воспользуйтесь содержанием ниже.

---
## Начало работы

Для старта обучения перейдите к [Группе 1 — Введение в Solana](learning/Lesson_1.md)

---

## Содержание

### Группа 1 — Введение в Solana (понятия и сети)

#### Подгруппа 1.1 — Общая картина
- [Урок 1 — Что такое Solana и почему она особенная](learning/Lesson_1.md)
- [Урок 2 — Основные сущности: аккаунты, программы, транзакции, инструкции](learning/Lesson_2.md)

#### Подгруппа 1.2 — Сети и окружения
- [Урок 3 — Devnet / Testnet / Mainnet — когда и зачем использовать каждую сеть](learning/Lesson_3.md)
- [Урок 4 — RPC и WebSocket — как клиент общается с цепочкой](learning/Lesson_4.md)

### Группа 2 — Инструменты и минимальный стек (solana-cli, test-validator, библиотеки)

#### Подгруппа 2.1 — CLI и локальная песочница
- [Урок 5 — solana-cli: основные команды (keygen, airdrop, balance, transfer)](learning/Lesson_5.md)
- [Урок 6 — solana-test-validator: локальная сеть для разработки](learning/Lesson_6.md)

#### Подгруппа 2.2 — Python-стек: solana и solders
- [Урок 7 — Знакомство с solana (возможности, уровни API)](learning/Lesson_7.md)
- [Урок 8 — Знакомство с solders (типы: Pubkey, Keypair, структуры)](learning/Lesson_8.md)

### Группа 3 — Ключи, кошельки, подписи (безопасность на старте)

#### Подгруппа 3.1 — Keypair и форматы
- [Урок 9 — Генерация Keypair и представления ключей (raw, hex, base58)](learning/Lesson_9.md)
- [Урок 10 — Seed / Mnemonic: восстановление и импорт](learning/Lesson_10.md)

#### Подгруппа 3.2 — Хранение и подписи
- [Урок 11 — Подпись транзакций: как и почему подписываем](learning/Lesson_11.md)
- [Урок 12 — Безопасное хранение ключей: файлы, шифрование, HSM концепт](learning/Lesson_12.md)

### Группа 4 — Простые операции: SOL, транзакции, подтверждения

#### Подгруппа 4.1 — Базовые переводы
- [Урок 13 — Airdrop в devnet и проверка баланса через RPC (минимум кода)](learning/Lesson_13.md)
- [Урок 14 — Перевод SOL: собрать, подписать, отправить, дождаться confirmation](learning/Lesson_14.md)

#### Подгруппа 4.2 — Надёжность транзакций
- [Урок 15 — Commitment levels: processed / confirmed / finalized — разница и выбор](learning/Lesson_15.md)
- [Урок 16 — Fees и оптимизация расходов (оценка и расчёт)](learning/Lesson_16.md)

### Группа 5 — Продвинутые транзакционные паттерны

#### Подгруппа 5.1 — Сложные сборки транзакций
- [Урок 17 — Несколько инструкций в одной транзакции (batching)](learning/Lesson_17.md)
- [Урок 18 — Частичная подпись (partial signing) и мульти-подписи на уровне клиента](learning/Lesson_18.md)

#### Подгруппа 5.2 — Nonce и устойчивость
- [Урок 19 — Durable Nonce: зачем нужен и как использовать](learning/Lesson_19.md)
- [Урок 20 — Retry-политики и дедупликация транзакций](learning/Lesson_20.md)

### Группа 6 — SPL Tokens: создание, хранение, передача

#### Подгруппа 6.1 — Концепция SPL токена
- [Урок 21 — Что такое SPL Token и Associated Token Account (ATA)](learning/Lesson_21.md)
- [Урок 22 — Создание (mint) нового SPL токена на devnet](learning/Lesson_22.md)

#### Подгруппа 6.2 — Операции с токенами
- [Урок 23 — Создать ATA и перевести токен (mint→ATA→transfer)](learning/Lesson_23.md)
- [Урок 24 — Burn, freeze, смена authority — безопасные операции](learning/Lesson_24.md)

### Группа 7 — Работа с аккаунтами, PDA и rent

#### Подгруппа 7.1 — Account internals
- [Урок 25 — Структура account: owner, lamports, data — чтение через RPC](learning/Lesson_25.md)
- [Урок 26 — Rent-exemption: зачем нужен и как рассчитывать депозит](learning/Lesson_26.md)

#### Подгруппа 7.2 — PDA (Program Derived Address)
- [Урок 27 — PDA: концепт, seeds и почему PDA нельзя контролировать приватным ключом](learning/Lesson_27.md)
- [Урок 28 — Использование PDA для хранения состояния программы](learning/Lesson_28.md)

### Группа 8 — Сериализация данных (Borsh, ручная упаковка)

#### Подгруппа 8.1 — Borsh и схемы
- [Урок 29 — Borsh: базовый принцип и почему его часто используют](learning/Lesson_29.md)
- [Урок 30 — Anchor layouts vs чистая Borsh: отличия и совместимость](learning/Lesson_30.md)

#### Подгруппа 8.2 — Ручная упаковка (struct/struct.pack)
- [Урок 31 — Ручная сериализация: struct.pack, endianess, выравнивание](learning/Lesson_31.md)
- [Урок 32 — Стратегии версионирования структуры данных on-chain](learning/Lesson_32.md)

### Группа 9 — Взаимодействие с программами (инструкции, CPI)

#### Подгруппа 9.1 — Создание инструкций
- [Урок 33 — Instruction: формирование accounts list и data payload](learning/Lesson_33.md)
- [Урок 34 — Примеры вызовов системной программы, Token Program и Metadata Program](learning/Lesson_34.md)

#### Подгруппа 9.2 — CPI и межпрограммные вызовы
- [Урок 35 — CPI (Cross-Program Invocation): концепция и ограничения](learning/Lesson_35.md)
- [Урок 36 — Логи, возвращаемые данные и отладка программ через RPC](learning/Lesson_36.md)

### Группа 10 — Тестирование и локальная разработка (CI)

#### Подгруппа 10.1 — Локальная разработка
- [Урок 37 — Поднятие test-validator с кастомными account/скриптами](learning/Lesson_37.md)
- [Урок 38 — Снапшоты и восстановление состояния test-validator](learning/Lesson_38.md)

#### Подгруппа 10.2 — Тесты и CI
- [Урок 39 — Unit-тесты: мокать RPC и проверять сборку инструкций](learning/Lesson_39.md)
- [Урок 40 — Integration-тесты: запуск на test-validator в CI (GitHub Actions)](learning/Lesson_40.md)

### Группа 11 — Архитектура dApp и оффчейн компоненты

#### Подгруппа 11.1 — Индексация и оффчейн хранилище
- [Урок 41 — Почему нужен indexer: события, state и searchability](learning/Lesson_41.md)
- [Урок 42 — Простая реализация indexer на Python (polling vs websocket)](learning/Lesson_42.md)

#### Подгруппа 11.2 — Backend patterns
- [Урок 43 — RPC pool и переключение провайдеров (fallback, priority)](learning/Lesson_43.md)
- [Урок 44 — Очереди задач и фоновые воркеры (mass payouts, reconciliation)](learning/Lesson_44.md)

### Группа 12 — Масштабирование, кеширование и оптимизация

#### Подгруппа 12.1 — Производительность
- [Урок 45 — Кеширование (TTL) для балансов и метаданных](learning/Lesson_45.md)
- [Урок 46 — Батчинг чтений и векторные запросы RPC](learning/Lesson_46.md)

#### Подгруппа 12.2 — Экономика операций
- [Урок 47 — Измерение затрат: fee, storage, off-chain costs](learning/Lesson_47.md)
- [Урок 48 — Параллелизм в клиенте: как не перегружать RPC и сохранять порядок](learning/Lesson_48.md)

### Группа 13 — Безопасность приложений и аудит кода

#### Подгруппа 13.1 — Управление ключами и секретами
- [Урок 49 — Vault/HSM/Secrets managers: концепты и интеграция](learning/Lesson_49.md)
- [Урок 50 — Ротация ключей и аварийное реагирование (compromise plan)](learning/Lesson_50.md)

#### Подгруппа 13.2 — Аудит и тестирование безопасности
- [Урок 51 — Статический анализ клиентского кода и dependency checks](learning/Lesson_51.md)
- [Урок 52 — Pen-tests, fuzzing и тесты на некорректные входы](learning/Lesson_52.md)

### Группа 14 — Обновляемые программы, governance и безопасность программ

#### Подгруппа 14.1 — Upgradable programs
- [Урок 53 — Принцип обновляемых программ (BPFLoaderUpgradeable)](learning/Lesson_53.md)
- [Урок 54 — Минимизация рисков при обновлении (timelock, multisig)](learning/Lesson_54.md)

#### Подгруппа 14.2 — Governance и контроль доступа
- [Урок 55 — Governance модели (on-chain голосования, multisig)](learning/Lesson_55.md)

### Группа 15 — NFT, метаданные и marketplaces (практически)

#### Подгруппа 15.1 — NFT basics
- [Урок 56 — NFT стандарты на Solana: метаданные, off-chain storage (IPFS)](learning/Lesson_56.md)
- [Урок 57 — Mint NFT и update metadata (процесс и права)](learning/Lesson_57.md)

#### Подгруппа 15.2 — Marketplace logic (off-chain orderbook + on-chain settlement)
- [Урок 58 — Дизайн простого marketplace: оффчейн ордеры + on-chain settlement](learning/Lesson_58.md)

### Группа 16 — DEX & AMM концепты (высшего уровня)

#### Подгруппа 16.1 — Понятия DEX
- [Урок 59 — Orderbook vs AMM: принципы и trade-offs на Solana](learning/Lesson_59.md)
- [Урок 60 — Liquidity, slippage, price-impact — как считать и минимизировать](learning/Lesson_60.md)

#### Подгруппа 16.2 — Интеграция с существующими протоколами
- [Урок 61 — Вызов Serum/Aggregators: интеграция через инструкции и CPI](learning/Lesson_61.md)

### Группа 17 — Масштабные практические проекты (capstone)

#### Подгруппа 17.1 — Проекты для портфолио
- [Урок 62 — Проект: минимальный кошелёк на Python (create/import/send)](learning/Lesson_62.md)
- [Урок 63 — Проект: индексер-трансферов с webhook-уведомлениями](learning/Lesson_63.md)

#### Подгруппа 17.2 — Сложные проекты
- [Урок 64 — Проект: простой NFT-gallery (чтение metadata + показы)](learning/Lesson_64.md)
- [Урок 65 — Проект: оффчейн orderbook + on-chain settlement (мини-DEX)](learning/Lesson_65.md)
- [Урок 66 — Проект: массовые выплаты (пул + idempotency + retry)](learning/Lesson_66.md)

### Группа 18 — Карьерный трек, open-source и подготовка к интервью

#### Подгруппа 18.1 — Резюме и портфолио
- [Урок 67 — Как оформить проекты и README, чтобы их понял рекрутер](learning/Lesson_67.md)
- [Урок 68 — Что показывать в интервью: топ-10 тем по Solana для backend-разработчика](learning/Lesson_68.md)

#### Подгруппа 18.2 — Open-source и вклад
- [Урок 69 — Как участвовать в OSS проектах экосистемы Solana](learning/Lesson_69.md)
- [Урок 70 — Как поддерживать production-репозиторий: release notes, changelog, semantic versioning](learning/Lesson_70.md)

### Группа 19 — Правила соответствия и операции (ops)

#### Подгруппа 19.1 — Регуляции и бухгалтерия
- [Урок 71 — Корпоративные требования: KYC/AML (вводные)](learning/Lesson_71.md)

#### Подгруппа 19.2 — Операционные процедуры
- [Урок 72 — Runbook: мониторинг, алерты, incident response для production dApp](learning/Lesson_72.md)

---

# Disclaimer (Отказ от ответственности)

Все описания, концепции, схемы, алгоритмы, примеры кода, расчёты, учебные планы и методические материалы, представленные в данном руководстве, подготовлены в целях обучения и демонстрации принципов работы экосистемы Solana.

Авторы курса прилагают все разумные усилия для обеспечения точности и актуальности информации.  
Тем не менее ответственность за проверку корректности, полноты и применимости приведённых данных лежит на читателе.

Материалы данного проекта **не являются инвестиционным советом**, коммерческим предложением или гарантией финансового результата.  
Использование примеров кода, описанных методов и инструментов осуществляется **на собственный риск** пользователя.

---


*Курс постоянно обновляется в соответствии с изменениями в экосистеме Solana*
---

© 2025 — Solana Developer Guide  
Автор: [Stanislav1710 - Solana Learning](https://github.com/Stanislav1710)

