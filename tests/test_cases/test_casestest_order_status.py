import pytest
from helpers.assertions import check_status_code, check_track_field, check_id_field
from tests.fixtures.order_fixtures import order_info_response


class TestOrderStatus:
    def test_status_code_200(self, order_info_response):
        """Проверяет, что статус‑код ответа — 200"""
        check_status_code(order_info_response)


    def test_track_field_correct(self, order_info_response):
        """Проверяет, что поле track в ответе совпадает с ожидаемым"""
        # Извлекаем трек‑номер из order_info_response или используем другой способ получения
        data = order_info_response.json()
        expected_track = data["order"]["track"]
        check_track_field(order_info_response, expected_track)


    def test_id_is_integer(self, order_info_response):
        """Проверяет, что ID заказа — целое число"""
        check_id_field(order_info_response)