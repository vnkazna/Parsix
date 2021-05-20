import socket
import selectors
import ssl
import re
from Parsix import parser
import json 

selector = selectors.DefaultSelector() # Определяем селектор данных по умолчанию для различных ОС


def server(): # Объявляем функцию создающую серверный сокет
    s_socket = ssl.wrap_socket(socket.socket(), 'private.pem', 'selfsigned.pem', ssl_version=ssl.PROTOCOL_TLSv1, server_side=True) # Делаем SSL(TLS) обертку для слушающего серверного сокета
    s_socket.bind(('localhost', 8443)) # Создаем привязку сокета
    s_socket.listen() # Ставим на прослушивание
    print('Started listening port 8443...\nWaiting data...')
    selector.register(fileobj=s_socket, events=selectors.EVENT_READ, data=con_accept) # Селектор данных


def con_accept(s_socket): # Создаем функцию принимающую клиентский сокет
    cl_socket, addr = s_socket.accept()
    print('Connection established on port 8443 from', addr, '\nReceiving and analizing data...')

    selector.register(fileobj=cl_socket, events=selectors.EVENT_READ, data=sender)


def sender(cl_socket): # Создаем функцию для первичной обработки данных из клиентского сокета    

    data_to_analize = cl_socket.recv(4096).decode('utf-8', 'ignore')
    
    if data_to_analize: # Проверяем наличие данных в буфере
        response = 'Server receiving and analizing data\n'.encode()
        cl_socket.send(response) # Отвечаем на принятые данные
        analize(data_to_analize) # Запускаем обработку 
    else:
        selector.unregister(cl_socket) # Отменяем регистрацию селектора данных
        cl_socket.close() # Закрываем соединение

 
def loop(): # Создаем функцию основного цикла
    while True:
        
        events = selector.select() # Создаем маркер появления данных в буфере
        for key, _ in events: # Итерируем список событий
            callback = key.data # Создаем объект обратного вызова с помощью метода data
            callback(key.fileobj) # Производим обратный вызов по зарегистрированным селекторам

def analize(data_to_analize): # Создаем функцию, которая будет принимать данные для анализа

    output_data = parser.parse_it(data_to_analize) # Для анализа обращаемся к модулю, разработанному ранее и установленному в составе пакета Parsix 
    #print(output_data)
    with open("parsered.json", "a+") as pr: 
        json.dump(output_data, pr)


if __name__ == '__main__': # Задаем точку входа в приложение
    server()
    loop()