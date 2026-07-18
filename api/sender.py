import requests
from . import config
from . import data

def post_new_order():
    """Создаёт новый заказ и возвращает ответ API."""
    try:
        response = requests.post(
            config.URL_SERVICE + config.CREATE_NEW_ORDER,
            json=data.new_order_body
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Ошибка при создании заказа: {e}")
        raise

def get_track_number(new_order_response):
    """Извлекает трек‑номер из ответа API."""
    try:
        json_data = new_order_response.json()
        track = json_data["track"]
        return track
    except ValueError as e:
        print("Ответ не в формате JSON")
        raise
    except KeyError as e:
        print(f"Поле 'track' не найдено в ответе: {json_data}")
        raise

def get_order_info(track):
    """Получает информацию о заказе по трек‑номеру."""
    try:
        response = requests.get(
            config.URL_SERVICE + config.GET_ORDER_INFO + "?t=" + str(track)
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Ошибка при получении информации о заказе {track}: {e}")
        raise

def delete_order(track):
    """Удаляет заказ по трек‑номеру."""
    try:
        response = requests.delete(
            config.URL_SERVICE + config.DELETE_ORDER + "?t=" + str(track)
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Ошибка при удалении заказа {track}: {e}")
        raise 