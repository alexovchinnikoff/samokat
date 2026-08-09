# tests/conftest.py
import pytest
# ВАЖНО: Импортируем напрямую из scooters_api, так как sender.py удален
from api.scooters_api import create_order, get_order_info, delete_order
from data.order_data import new_order_body

@pytest.fixture
def test_order():
    """
    Фикстура: создаёт тестовый заказ, возвращает трек-номер.
    Гарантированно удаляет заказ после завершения теста.
    """
    track = None

    # --- SETUP: Создание заказа ---
    try:
        # Используем данные из data/order_data.py
        response = create_order(new_order_body)
        
        print(f"🚀 Создан заказ. Статус: {response.status_code}")
        
        if response.status_code not in [200, 201]:
            pytest.fail(f"❌ Не удалось создать заказ. Статус: {response.status_code}, Ответ: {response.text}")

        # Парсим трек-номер из ответа
        data = response.json()
        track = data.get("track") # Или как называется поле в твоем API
        
        if not track:
            pytest.fail("❌ В ответе API не найден трек-номер заказа")
            
    except Exception as e:
        pytest.fail(f"❌ Ошибка при создании заказа: {e}")

    # Передаем трек-номер в тест
    yield track

    # --- TEARDOWN: Очистка (удаление заказа) ---
    # Этот блок выполнится ВСЕГДА, даже если тест упал
    if track:
        try:
            print(f"🧹 Удаляем тестовый заказ: {track}")
            delete_response = delete_order(track)
            
            if delete_response.status_code != 200:
                print(f"⚠️ Предупреждение: заказ {track} не был удален (статус {delete_response.status_code})")
                # Не делаем pytest.fail здесь, чтобы не ломать сам тест очистки, 
                # но логируем проблему.
        except Exception as e:
            print(f"⚠️ Ошибка при удалении заказа {track}: {e}")

@pytest.fixture
def order_info_response(test_order):
    """
    Получает информацию о заказе по трек-номеру.
    Зависит от фикстуры test_order (которая уже создала заказ).
    """
    track = test_order
    response = get_order_info(track)
    
    if response.status_code != 200:
        pytest.fail(f"❌ Не удалось получить информацию о заказе {track}. Статус: {response.status_code}")
        
    return response
