# conftest.py
import pytest
from api.sender import post_new_order, get_track_number, get_order_info, delete_order


@pytest.fixture
def test_order():
    """
    Фикстура: создаёт тестовый заказ и возвращает трек‑номер.
    После выполнения теста удаляет созданный заказ.
    Returns:
        str: трек‑номер созданного заказа
    """
    track = None  # Инициализируем track заранее


    # Создание заказа
    try:
        response = post_new_order()
        print(f"Order creation response: {response.status_code} - {response.text}")

        if response.status_code not in [200, 201]:
            pytest.fail(f"Failed to create test order: {response.status_code} {response.text}")


        # Извлечение трек‑номера
        track = get_track_number(response)
        if track is None:
            pytest.fail("Track number not found in response")
    except Exception as e:
        pytest.fail(f"Exception during order creation: {e}")


    yield track  # Теперь track всегда определена


    # Очистка: удаление созданного заказа после теста
    if track is not None:  # Проверяем, что track создан
        try:
            delete_response = delete_order(track)
            if delete_response.status_code != 200:
                print(f"Warning: failed to delete test order {track}. Status: {delete_response.status_code}")
        except Exception as e:
            print(f"Warning: exception during order deletion {track}: {e}")



@pytest.fixture
def order_info_response(test_order):
    """
    Фикстура: получает информацию о заказе по трек‑номеру.
    Зависит от фикстуры test_order.
    Args:
        test_order (str): трек‑номер заказа (из фикстуры test_order)
    Returns:
        Response: ответ API с информацией о заказе
    """
    response = get_order_info(test_order)
    assert response.status_code == 200, f"Failed to get order info for track {test_order}"
    return response 
