import pytest
from helpers.assertions import check_delivery_date, check_timestamp_fields

@pytest.fixture
def new_order_body():
    return {
        "firstName": "Иван",
        "lastName": "Петров",
        "deliveryDate": "2024-12-31"
    }

class TestOrderDates:
    def test_delivery_date_correct(self, order_info_response, new_order_body):
        """Проверяет соответствие deliveryDate в ответе и запросе"""
        check_delivery_date(order_info_response, new_order_body)


    def test_timestamps_are_strings(self, order_info_response):
        """Проверяет, что временные метки — строки"""
        check_timestamp_fields(order_info_response) 