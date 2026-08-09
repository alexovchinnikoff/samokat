# tests/conftest.py
import pytest
from api.scooters_api import create_order, get_order_info, delete_order
from data.order_data import new_order_body

@pytest.fixture
def test_order():
    track = None

    try:
        # 1. Создаем заказ
        response = create_order(new_order_body)
        
        if response.status_code not in [200, 201]:
            pytest.fail(f"❌ Не удалось создать заказ. Статус: {response.status_code}, Ответ: {response.text}")

        # 2. ПРАВИЛЬНО достаем трек из вложенности
        data = response.json()
        
        # Твой ответ выглядит так: {"order": {"track": 123, ...}}
        # Поэтому сначала берем объект order, потом поле track
        order_data = data.get("order")
        
        if not order_data:
            pytest.fail("❌ В ответе API нет объекта 'order'")
            
        track = order_data.get("track")
        
        if not track:
            pytest.fail("❌ В объекте 'order' не найден трек-номер")
            
        print(f"✅ Заказ создан! Трек-номер: {track}")

    except Exception as e:
        pytest.fail(f"❌ Ошибка при создании заказа: {e}")

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
