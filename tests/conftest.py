import pytest
from api.sender import post_new_order, get_track_number, get_order_info
from api.data import new_order_body

# === ФИКСТУРЫ ===

@pytest.fixture
def test_order():
    """
    Создаёт тестовый заказ перед тестом.
    Возвращает трек‑номер.
    После теста можно добавить очистку (удаление заказа).
    """
    response = post_new_order()
    track = get_track_number(response)
    yield track
    # Здесь можно добавить код для удаления заказа после теста

@pytest.fixture
def order_info_response(test_order):
    """
    Получает полную информацию о заказе по трек‑номеру.
    Зависит от фикстуры test_order.
    """
    return get_order_info(test_order)

@pytest.fixture
def sample_order_data():
    """
    Возвращает шаблон данных для создания заказа.
    Можно использовать в разных тестах.
    """
    return new_order_body.copy()

# === ХУКИ ДЛЯ PYTEST ===

def pytest_configure(config):
    """Выводится один раз при старте всех тестов"""
    print("\n🚀 Запуск тестов API Самоката...")
    print("🔎 Проверяем получение информации о заказе")

def pytest_runtest_setup(item):
    """Выводится перед каждым тестом"""
    test_name = item.name.replace("test_", "").replace("_", " ").title()
    print(f"\n🧪 Запуск теста: {test_name}")

def pytest_terminal_summary(terminalreporter):
    """Формирует отчёт в конце всех тестов"""
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    total = passed + failed

    print(f"\n{'='*50}")
    print("📊 ФИНАЛЬНЫЙ ОТЧЁТ")
    print(f"Всего тестов: {total}")
    print(f"✅ Пройдено: {passed}")
    print(f"❌ Упало: {failed}")

    if failed == 0:
        print("🎉 Все тесты пройдены успешно!")
    else:
        print(f"⚠️  Обнаружены проблемы в {failed} тестах")
    print(f"{'='*50}")

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (если нужны в нескольких тестах) ===

def create_order_with_params(**kwargs):
    """
    Вспомогательная функция для создания заказа с кастомными параметрами.
    Пример использования:
    custom_order = create_order_with_params(firstName="Анна", lastName="Иванова")
    """
    order_data = new_order_body.copy()
    order_data.update(kwargs)
    # Здесь должна быть логика отправки запроса с обновлёнными данными
    # response = requests.post(url, json=order_data, ...)
    # return get_track_number(response)
    return order_data  # упрощённый возврат для примера 