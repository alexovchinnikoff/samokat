# 🛴 Структура проекта Samokat QA

Это репозиторий с автотестами для API сервиса «Самокат». Проект организован по модульному принципу: отдельные папки для тестов, логики API, тестовых данных и артефактов.

## 📂 Дерево файлов

```text
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
