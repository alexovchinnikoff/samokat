# scooters_api.py
import requests
import httpx
from api.config import (
    URL_SERVICE,
    CREATE_COURIER,
    LOGIN_COURIER,
    DELETE_COURIER,
    CREATE_NEW_ORDER,
    GET_ORDER_INFO,
    DELETE_ORDER
)

TIMEOUT = 10.0  # Таймаут в секундах


def create_courier(payload):
    """Создаёт нового курьера."""
    url = URL_SERVICE + CREATE_COURIER
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    print(f"Creating courier: POST {url}")  # Отладка: URL
    print(f"Payload: {payload}")  # Отладка: данные

    print(f"Response status: {response.status_code}")  # Отладка: статус
    return response


def login_courier(payload):
    """Авторизует курьера и возвращает его ID."""
    url = URL_SERVICE + LOGIN_COURIER
    print(f"Logging in courier: POST {url}")  # Отладка: URL
    print(f"Payload: {payload}")  # Отладка: данные
    response = requests.post(url, json=payload, timeout=TIMEOUT)
    print(f"Response status: {response.status_code}")  # Отладка: статус
    return response

def delete_courier(courier_id):
    """Удаляет курьера по ID."""
    courier_id_str = str(courier_id)  # Гарантируем строковый тип
    url = URL_SERVICE + DELETE_COURIER + courier_id_str
    print(f"Deleting courier: DELETE {url}")  # Отладка: URL
    response = requests.delete(url, timeout=TIMEOUT)
    print(f"Response status: {response.status_code}")  # Отладка: статус
    return response

def create_order(payload):
    """Создаёт новый заказ."""
    url = URL_SERVICE + CREATE_NEW_ORDER
    print(f"Creating order: POST {url}")  # Отладка: URL
    print(f"Payload: {payload}")  # Отладка: данные
    response = requests.post(url, json=payload, timeout=TIMEOUT)
    print(f"Response status: {response.status_code}")  # Отладка: статус
    return response

def get_order_info(track_number):
    """Получает информацию о заказе по трек‑номеру."""
    track_str = str(track_number)  # Гарантируем строковый тип
    url = URL_SERVICE + GET_ORDER_INFO + "/" + track_str
    print(f"Getting order info: GET {url}")  # Отладка: URL
    response = requests.get(url, timeout=TIMEOUT)
    print(f"Response status: {response.status_code}")  # Отладка: статус
    return response

def delete_order(track_number):
    """Удаляет заказ по трек‑номеру."""
    track_str = str(track_number)  # Гарантируем строковый тип
    url = URL_SERVICE + DELETE_ORDER + "/" + track_str
    print(f"Deleting order: DELETE {url}")  # Отладка: URL
    response = requests.delete(url, timeout=TIMEOUT)
    print(f"Response status: {response.status_code}")  # Отладка: статус
    return response 
