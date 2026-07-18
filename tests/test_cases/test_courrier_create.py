import pytest
import random
import string

from api.scooters_api import create_courier, login_courier, delete_courier

def generate_random_string(length, include_digits=False):
    """Генерирует случайную строку.
    
    Args:
        length (int): Длина строки.
        include_digits (bool): Если True, включает цифры, иначе — только буквы.
    
    Returns:
        str: Сгенерированная строка.
    """
    if include_digits:
        characters = string.ascii_letters + string.digits
    else:
        characters = string.ascii_letters
    
    return ''.join(random.choice(characters) for _ in range(length))

@pytest.fixture
def courier_data_and_cleanup():
    """Фикстура для подготовки данных курьера и их очистки после теста."""
    # --- Шаг 1: Подготовка данных (Setup) ---
    login = generate_random_string(5)  # Только английские буквы
    password = generate_random_string(10, include_digits=True)  # Буквы и цифры
    first_name = generate_random_string(6)  # Только английские буквы
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    print(f"Creating courier with login: {login}, password: {password}")
    yield payload  # Передаем данные в тест
    
    # --- Шаг 3: Очистка данных (Teardown) ---
    try:
        # Сначала авторизуемся, чтобы получить ID курьера
        login_payload = {"login": payload["login"], "password": payload["password"]}
        login_response = login_courier(login_payload)
        
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            delete_response = delete_courier(courier_id)
            
            if delete_response.status_code == 200:
                print(f"Courier {courier_id} deleted successfully")
            else:
                print(f"Failed to delete courier {courier_id}. Status: {delete_response.status_code}, Response: {delete_response.text}")
        else:
            print(f"Failed to login for cleanup. Status: {login_response.status_code}, Response: {login_response.text}")
    except Exception as e:
        print(f"Error during cleanup: {e}")


def test_create_courier_success(courier_data_and_cleanup):
    """
    Тест успешного создания курьера с автоматической очисткой данных.
    Проверяет:
    - статус-код 201
    - корректное тело ответа
    - возможность авторизации созданного курьера
    """
    # --- Шаг 2: Выполнение теста ---
    payload = courier_data_and_cleanup

    print(f"Sending POST to create courier: {payload}")  # Отладка
    response = create_courier(payload)


    # Проверка статус-кода
    assert response.status_code == 201, (
        f"Ожидался статус-код 201, но получен {response.status_code}. "
        f"URL: {getattr(response, 'url', 'Unknown')} "
        f"Response: {response.text}"
    )

    # Проверка тела ответа
    response_data = response.json()
    print(f"Response data: {response_data}")  # Отладка

    assert "ok" in response_data, "Ответ не содержит поле 'ok'"
    assert response_data["ok"] is True, f"Поле 'ok' должно быть True, получено: {response_data['ok']}"

    # Дополнительная проверка: пытаемся авторизоваться как созданный курьер
    login_payload = {
        "login": payload["login"],
        "password": payload["password"]
    }
    print(f"Attempting to login with: {login_payload}")  # Отладка

    login_response = login_courier(login_payload)
    assert login_response.status_code == 200, (
        f"Авторизация курьера не удалась: {login_response.status_code}. "
        f"Response: {login_response.text}"
    )
    login_data = login_response.json()
    assert "id" in login_data, "Ответ авторизации не содержит ID курьера"
    assert isinstance(login_data["id"], int), "ID курьера должен быть числом"


    print("Courier created and authenticated successfully") 