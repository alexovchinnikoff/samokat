# Александр Овчинников, 43-я когорта — Финальный проект. Инженер по тестированию расширенный
import config
import data
import requests
import sender
import random
import re

# импортируем функции
from sender import post_new_order, get_track_number, get_order_info

# проверяем результат успешного создания заказа
def positive_assert(track):
    get_order_info_response = get_order_info(track) # вводим новую переменную get_order_info_response и присваиваем ей значение - ответ на запрос с номером track
    assert get_order_info_response.status_code == 200 # Проверяем код ответа
    response_data = get_order_info_response.json()# вводим новую переменную response_data и присваиваем ей значение - тело ответа на запрос информации о заказе с данными о созданном заказе
    assert response_data["order"]["track"] == track # Проверяем что тело ответа содержит track с корректным значением
    assert isinstance(response_data["order"]["id"], int) # Проверяем что тело ответа содержит id внутри order со значением в integer
    assert response_data["order"]["firstName"] == data.new_order_body["firstName"] # Проверяем что тело ответа содержит firstName с корректным значением
    assert response_data["order"]["lastName"] == data.new_order_body["lastName"] # Проверяем что тело ответа содержит lastName с корректным значением
    assert response_data["order"]["metroStation"] == str(data.new_order_body["metroStation"]) # Проверяем что тело ответ содержит metroStation с корректным Строчным значением, т.к. в ответе строчное значение, а в запросе integer 
    assert response_data["order"]["rentTime"] == data.new_order_body["rentTime"] # Проверяем что тело ответа содержит rentTime с корректным значением
    server_date = response_data["order"]["deliveryDate"] # вводим новую переменную server_date и присваиваем ей значение даты на сервере (длинное)
    request_date = data.new_order_body["deliveryDate"] # вводим новую переменную request_date и присваиваем ей значение даты запроса (короткое)
    server_date_only = server_date.split('T')[0] # вводим новую переменную server_date_only и обрезаем длинное серверное значение до короткого (до Т)
    assert server_date_only == request_date # проверяем, что обрезанное значение совпадает со значением в запросе при создании заказа
    
    ###в рамках улучшения кода ИИ предлагает проверить соответствие формата даты, но предложенный вариант проверки может сломать тест в случае изменений временного формата на сервере
    #expected_format = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$' ##вводим новую переменную для дальнейшего сравнения форматов данных для deliveryDate, createdAt, updatedAt
    #assert re.match(expected_format, server_date), ## с помощью импортированного re сравниваем даты ###закомментил этот код, т.к. предложенный ИИ вариант проверки может поломать тест в случае изменений временного формата на сервере
    
    assert response_data["order"]["status"] == 0 #проверяем конкретное значение status для только что созданного заказа

    ###закомментил код, т.к. не думаю, что он уместен в рамках данного сценария.но в целом можно проверить разные значения status
    #if response_data["order"]["finished"] == True: #проверяем конкретное значение только что созданного заказа
       #assert response_data["order"]["status"] == -1
    #elif response_data["order"]["inDelivery"] == True:
       #assert response_data["order"]["status"] == 1
    #else:
       #assert response_data["order"]["status"] == 0    
              
    if "color" in response_data["order"]:#ввиду того, что color необязательный параметр и неизвестно тело ответа в случае создания заказа без него, допускаем, что color может отсутствовать
       assert response_data["order"]["color"] == data.new_order_body["color"] #если color в теле ответа, то проверяем значение в ответе, с тем, что было в запросе
    if "comment" in response_data["order"]:#ввиду того, что comment необязательный параметр и неизвестно тело ответа в случае создания заказа без него, допускаем, что comment может отсутствовать
       assert response_data["order"]["comment"] == data.new_order_body["comment"] #если comment в теле ответа, то проверяем значение в ответе, с тем, что было в запросе
       
    #assert isinstance(response_data["order"]["cancelled"], bool)#проверяем, что в теле ответа есть cancelled с булевым значением
    assert response_data["order"]["cancelled"] == False #для данного сценария проверяем конкретное значение

    #assert isinstance(response_data["order"]["finished"], bool)#проверяем, что в теле ответа есть finished с булевым значением
    assert response_data["order"]["finished"] == False #для данного сценария проверяем конкретное значение

    #assert isinstance(response_data["order"]["inDelivery"], bool)#проверяем, что в теле ответа есть inDelivery с булевым значением
    assert response_data["order"]["finished"] == False #для данного сценария проверяем конкретное значение

    if response_data["order"]["inDelivery"]:#проверяем случаи если заказ примут
       assert isinstance(response_data["order"]["courierFirstName"], str) #проверяем, что в теле ответа есть courierFirstName со стринговым значением, если заказ взят в работу курьером
    else:
       assert response_data["order"].get("courierFirstName", "") == "" #проверяем, что в теле ответа есть courierFirstName с пустым значением, если заказ не взят в работу курьером

    assert isinstance(response_data["order"]["createdAt"], str)#проверяем, что в ответе есть createdAt со значением в string
    #date_create = response_data["order"]["createdAt"]##
    #assert re.match(expected_format, date_create)## с помощью импортированного re сравниваем даты. но не в этом сценарии
    
    assert isinstance(response_data["order"]["updatedAt"], str)#проверяем, что в ответе есть updatedAt со значением в string
    #date_update = response_data["order"]["updatedAt"]##
    #assert re.match(expected_format, date_update) ## с помощью импортированного re сравниваем даты. но не в этом сценарии
    
# проверяем результат неуспешного создания набора (если нет трэк или некорректный)
def negative_assert_code_400(track): # объявляем функцию с параметрами
    get_order_info_response = get_order_info(track) # в новую переменную get_order_info_response помещает ответ на запрос информации о заказе
    assert get_order_info_response.status_code == 400 # Проверяем код ответа
    assert get_order_info_response.json()["message"] == "Недостаточно данных для поиска"# Проверяем что в теле ответа есть ответа сообщение

def negative_assert_code_404(track): # объявляем функцию с параметрами
    get_order_info_response = get_order_info(track) # в новую переменную get_order_info_response помещает ответ на запрос информации о заказе
    assert get_order_info_response.status_code == 404 # проверяем код ответа
    assert get_order_info_response.json()["message"] == "Заказ не найден"# Проверяем что в теле ответа есть ответа сообщение

# Тест_1_запускаем функцию проверки с тестовым значением параметра (Допустимое значение параметра)
def test_get_order_info_success_response():
    response = post_new_order()  # Создаем новый заказ и сохраняем в переменную созданный номер
    track = get_track_number(response)# Присваемаем переменной track результат работы функции по вычленению номера из ответа на запрос о создании заказа
    positive_assert(track) # Запускаем проверку с параметрами (с тестовым значением track)

# Тест_2_запускаем функцию проверки с тестовым значением параметра (пустой параметр)
def test_get_order_info_empty_param_400():
    track = ""
    negative_assert_code_400(track) # Запускаем проверку с параметрами (с тестовым значением track)

# Тест_3_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 1 символов)
def test_get_order_info_1number_param_404():
    track = random.randint(1, 9)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_4_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 3 символов)
def test_get_order_info_3numbers_param_404():
    track = random.randint(100, 999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_5_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 5 символов)
def test_get_order_info_5numbers_param_404():
    track = random.randint(10000, 99999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_6_запускаем функцию проверки с тестовым значением параметра (некорректный номер в корректном формате - 6 символов)
def test_get_order_6numbers_track_404():
    track = random.randint(100000, 999999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_7_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 7 символов)
def test_get_order_info_7numbers_param_404():
    track = random.randint(1000000, 9999999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# 500 ошибка возникает от 10 символов
# Тест_8_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 8 символов)
def test_get_order_info_8numbers_param_404():
    track = random.randint(10000000, 99999999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_9_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 9 символов)
def test_get_order_info_9numbers_param_404():
    track = random.randint(100000000, 999999999)
    negative_assert_code_404(track) # Запускаем проверку с параметром
# Тест_10_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 10 символов)
def test_get_order_info_10numbers_param_404():
    track = random.randint(1000000000, 9999999999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_11_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 11 символов)
def test_get_order_info_11numbers_param_404():
    track = random.randint(10000000000, 99999999999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_12_запускаем функцию проверки с тестовым значением параметра (некорректный номер в не корректном формате - 20 символов)
def test_get_order_info_20numbers_param_404():
    track = random.randint(10000000000000000000, 99999999999999999999)
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_13_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка русских букв)
def test_get_order_info_letters_param_400():
    track = "АБЫРВАЛГ"
    negative_assert_code_400(track) # Запускаем проверку с параметром

# Тест_14_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка с пробелом)
def test_get_order_info_space_param_400():
    track = "11 11"
    negative_assert_code_400(track) # Запускаем проверку с параметром

# Тест_15_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка с точкой)
def test_get_order_info_dot_param_400():
    track = "11.11"
    negative_assert_code_400(track) # Запускаем проверку с параметром

# Тест_16_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка с зпт)
def test_get_order_info_comma_param_400():
    track = "11,11"
    negative_assert_code_400(track) # Запускаем проверку с параметром

# Тест_17_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка в ковычках)
def test_get_order_info_cliffs_param_400():
    track = '"1111"'
    negative_assert_code_400(track) # Запускаем проверку с параметром

# Тест_18_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка с 0)
def test_get_order_info_zerosymbol_param_404():
    track = "0"
    negative_assert_code_404(track) # Запускаем проверку с параметром

# Тест_19_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка с отрицательным значением)
def test_get_order_info_minussymbol_param_400():
    track = "-1"
    negative_assert_code_400(track) # Запускаем проверку с параметром

# Тест_20_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка с спецсимволом)
def test_get_order_info_specsymb_param_400():
    track = "11?11"
    negative_assert_code_400(track) # Запускаем проверку с параметром

# Тест_21_запускаем функцию проверки с тестовым значением параметра (некорректный номер - строка с булевым значением)
def test_get_order_info_bool_param_400():
    track = "True"
    negative_assert_code_400(track) # Запускаем проверку с параметром