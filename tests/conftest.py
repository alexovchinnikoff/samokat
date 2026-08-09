# tests/conftest.py
import pytest
from api.scooters_api import create_order, get_order_info, delete_order
from data.order_data import new_order_body


@pytest.fixture
def test_order():
    track = None

    try:
        # 1. Создаем заказ
        print(f"🚀 Пытаемся создать заказ с данными: {new_order_body}")
        response = create_order(new_order_body)

        # 2. ВАЖНО: Выводим полный сырой ответ сервера в консоль
        # Это поможет тебе увидеть реальную структуру или ошибку
        print("-" * 40)
        print("📡 ОТВЕТ ОТ СЕРВЕРА (JSON):")
        try:
            print(response.json())
        except:
            print(response.text)  # Если это не JSON (например, HTML страница ошибки)
        print("-" * 40)

        # 3. Проверка статуса
        if response.status_code not in [200, 201]:
            pytest.fail(f"❌ Статус не 200/201. Получено: {response.status_code}. Ответ: {response.text}")

        # 4. Парсинг трека (универсальный вариант)
        data = response.json()

        # Логика: пробуем найти трек в разных местах, чтобы тест не падал сразу
        if "order" in data:
            order_data = data["order"]
            track = order_data.get("track")
        elif "track" in data:
            track = data.get("track")
        else:
            # Если структура совсем другая, выводим ключи, чтобы понять, что там есть
            print(f"⚠️ Неизвестная структура ответа. Ключи: {list(data.keys())}")
            pytest.fail("❌ Не удалось найти трек-номер в ответе API")

        if not track:
            pytest.fail("❌ В ответе API не найден трек-номер")

    except Exception as e:
        pytest.fail(f"❌ Критическая ошибка при создании заказа: {e}")

    yield track

    # 3. Очистка (удаление заказа)
    if track:
        try:
            print(f"🧹 Удаляем тестовый заказ: {track}")
            delete_response = delete_order(track)

            if delete_response.status_code != 200:
                print(f"⚠️ Предупреждение: заказ {track} не был удален (статус {delete_response.status_code})")
        except Exception as e:
            print(f"⚠️ Ошибка при удалении заказа {track}: {e}")


@pytest.fixture
def order_info_response(test_order):
    track = test_order
    response = get_order_info(track)

    if response.status_code != 200:
        pytest.fail(f"❌ Не удалось получить информацию о заказе {track}. Статус: {response.status_code}")

    return response
