# 🛴 Структура проекта Samokat QA

Это репозиторий с автотестами для API сервиса «Самокат». Проект организован по модульному принципу: отдельные папки для тестов, логики API, тестовых данных и артефактов.

## 📂 Дерево файлов

```text
D:\Projects\samokat_root\samokat-third/
├── .gitignore                # Игнорирует venv, отчеты, логи
├── requirements.txt          # Список библиотек (pytest, requests, allure-pytest)
├── README.md                 # Описание проекта, статус, как запустить, результаты
│
├── .venv/                    # Виртуальное окружение (создается командой python -m venv .venv)
│   └── ...                   # (внутренние файлы venv, их не трогаем)
│
├── api/                      # 🌐 Слой работы с API (чистые запросы)
│   ├── __init__.py
│   ├── config.py             # URL стенда и пути к эндпоинтам
│   └── scooters_api.py      # Функции: create_order, get_order_info, delete_order и т.д.
│
├── data/                     # 📦 Тестовые данные (шаблоны JSON)
│   ├── __init__.py
│   └── order_data.py         # Словарь new_order_body с данными для теста
│
├── helpers/                  # 🧰 Вспомогательные функции (ассерты, утилиты)
│   ├── __init__.py
│   ├── assertions.py         # Функции проверок: check_customer_info, check_delivery_date и т.д.
│   └── utils.py              # Генераторы случайных строк, дат и т.п.
│
├── tests/                    # 🧪 Тесты и фикстуры
│   ├── __init__.py
│   ├── conftest.py          # ГЛАВНЫЙ ФАЙЛ: фикстуры test_order, order_info_response, хуки
│   │                         # (автоматически подхватываются всеми тестами)
│   └── test_cases/          # Папка с самими тестами
│       ├── __init__.py
│       ├── test_casestest_order_customer.py
│       ├── test_casestest_order_dates.py
│       ├── test_casestest_order_optional.py
│       ├── test_casestest_order_status.py
│       └── test_courrier_create.py
│
├── allure-results/          # 📊 Сюда сохраняются сырые данные для отчета Allure (создается при запуске)
│
├── report.html               # 📄 Красивый HTML-отчет (создается командой --html)
│
└── logs/                     # 📜 Логи выполнения тестов (если настроишь логирование) 
D:\Projects\samokat_root/
├── .gitignore                # (обязательно создай этот файл!)
├── requirements.txt          # Список библиотек для установки
├── run_tests.bat             # Скрипт запуска (для Windows)
│
├── api/                      # 🌐 Логика работы с API (не сами тесты!)
│   ├── __init__.py
│   ├── config.py             # URL стенда, заголовки, токены
│   ├── sender.py            # Функции отправки GET/POST/PATCH запросов
│   └── scooters_api.py      # Обертки: "создать заказ", "получить курьера"
│
├── data/                     # 📦 Только данные (JSON, словари, классы данных)
│   ├── __init__.py
│   └── order_data.py        # Шаблоны тел запросов (payloads)
│
├── tests/                    # 🧪 Только тесты (ничего лишнего!)
│   ├── __init__.py
│   ├── conftest.py          # Фикстуры (setup/teardown, общие переменные)
│   ├── test_cases/          # Сами файлы с тестами
│   │   ├── __init__.py
│   │   ├── test_casestest_order_customer.py
│   │   ├── test_casestest_order_dates.py
│   │   ├── test_casestest_order_optional.py
│   │   ├── test_casestest_order_status.py
│   │   └── test_courrier_create.py
│   ├── helpers/             # Вспомогательные функции (assertions, utils)
│   │   ├── __init__.py
│   │   ├── assertions.py    # Твои кастомные проверки (если нужны)
│   │   └── utils.py         # Генераторы случайных данных и т.д.
│   │
│   ├── reports/              # Сюда Allure будет складывать отчеты
│   │   └── latest/          # (папка создастся автоматически при запуске)
│   └── logs/                # Сюда можно писать свои логи
│
├── allure-results/           # (папка создастся автоматически при запуске)
└── README.md                # Описание проекта (как мы делали выше)
