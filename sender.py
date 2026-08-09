import config
import data
import requests

# функция для отправки POST-запроса на создание нового заказа
def post_new_order():
    return requests.post(config.URL_SERVICE + config.CREATE_NEW_ORDER,
                         json=data.new_order_body)

def get_track_number(new_order_response): # функция для использования ответа объявляем функцию с параметром new_order_response
    track = new_order_response.json()["track"] # вводим новую переменную track и присваиваем ей номер из ответа сервера на создание нового заказа (new order response зададим к коде)
    return track # возвращаем новое значение переменной

# функция для отправки GET-запроса на получение информации о заказе по его номеру
def get_order_info(track):
    return requests.get(config.URL_SERVICE + config.GET_ORDER_INFO + "?t=" + str(track))
