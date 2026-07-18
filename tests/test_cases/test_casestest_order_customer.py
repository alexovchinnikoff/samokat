import pytest
from helpers.assertions import check_customer_info

@pytest.fixture
def new_order_body():
    return {
        "firstName": "Иван",
        "lastName": "Петров",
        "deliveryDate": "2024-12-31"
    }

class TestOrderCustomerInfo:
    def test_customer_name_correct(self, order_info_response, new_order_body):
        """Проверяет корректность имени и фамилии клиента в ответе"""
        check_customer_info(order_info_response, new_order_body) 