# api/scooters_api.py
import requests
from .config import (
    URL_SERVICE,
    CREATE_COURIER,
    LOGIN_COURIER,
    DELETE_COURIER,
    CREATE_NEW_ORDER,
    GET_ORDER_INFO,
    DELETE_ORDER
)

TIMEOUT = 10.0

def create_courier(payload):
    url = URL_SERVICE + CREATE_COURIER
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    return response

def login_courier(payload):
    url = URL_SERVICE + LOGIN_COURIER
    response = requests.post(url, json=payload, timeout=TIMEOUT)
    return response

def delete_courier(courier_id):
    courier_id_str = str(courier_id)
    url = URL_SERVICE + DELETE_COURIER + courier_id_str
    response = requests.delete(url, timeout=TIMEOUT)
    return response

def create_order(payload):
    url = URL_SERVICE + CREATE_NEW_ORDER
    response = requests.post(url, json=payload, timeout=TIMEOUT)
    return response

def get_order_info(track_number):
    """
    ВАЖНО: Эндпоинт работает через query-параметр ?t=
    Пример URL: https://qa-scooter.praktikum-services.ru/api/v1/orders/track?t=123456
    """
    track_str = str(track_number)
    # Формируем URL с параметром t
    url = f"{URL_SERVICE}{GET_ORDER_INFO}?t={track_str}"
    
    response = requests.get(url, timeout=TIMEOUT)
    return response

def delete_order(track_number):
    track_str = str(track_number)
    # Для удаления тоже используем параметр t, судя по твоей логике
    url = f"{URL_SERVICE}{DELETE_ORDER}?t={track_str}"
    response = requests.delete(url, timeout=TIMEOUT)
    return response
