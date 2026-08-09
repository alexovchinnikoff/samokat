# test_casestest_order_optional.py
import pytest
from helpers.assertions import check_optional_fields, check_boolean_fields, check_courier_field

from helpers.assertions import (
    check_optional_fields,
    check_boolean_fields,
    check_courier_field
)
from tests.fixtures.order_fixtures import order_info_response, test_order


class TestOrderOptionalFields:
    """Проверяет опциональные поля color и comment, если они есть в ответе"""


    @pytest.fixture
    def new_order_body(self):
        return {
            "firstName": "Иван",
            "lastName": "Петров",
            "deliveryDate": "2024-12-31",
            "color": "red",
            "comment": "Test comment"
        }

    def test_optional_fields_if_present(self, order_info_response, new_order_body):
        """Проверяет опциональные поля color и comment, если они есть в ответе"""
        check_optional_fields(order_info_response, new_order_body)


    def test_boolean_fields_correct(self, order_info_response):
        """Проверяет булевые поля cancelled и finished"""
        check_boolean_fields(order_info_response)

    def test_courier_field_depends_on_status(self, order_info_response):
        """Проверяет поле courierFirstName в зависимости от статуса заказа"""
        check_courier_field(order_info_response)
