import time
import socket
import base64
import threading


class Server:
    def __init__(self, ip, port):
        self.ip = ip # IP Сервера
        self.port = port # Port Сервера
        self.all_client = [] # База пользователей чата
        
        # Запускаем прослушивание соединений
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port)) # Начала прослушование по определенному ip порту
        self.server.listen(0) # Максимальное количество пользовотелей, которое может обслуживать сервер (При значение "0", пользователей неограниченное количество)
        threading.Thread(target=self.connect_handler).start() # Запуск потока для отслеживания новых соеденений 
        print('Сервер запущен!')
        

    # Обрабатываем входящие соединения
    def connect_handler(self):
        while True:
            client, address = self.server.accept()
            if client not in self.all_client: # Проверка пользователя на наличие его в чате
                self.all_client.append(client) 
                threading.Thread(target=self.message_handler, args=(client,)).start() # Запуск потока для обработки сообщений 
                client.send('Успешное подключение к чату!'.encode('utf-8'))
            time.sleep(1)


    # Обрабатывание отправленного текста
    def message_handler(self, client_socket):
        while True:
            message = client_socket.recv(1024)
            print(message)

            # Удаление текущего сокета если пользователь напишет "exit"
            if message == b'exit': 
                self.all_client.remove(client_socket)
                break

            for client in self.all_client: # Отправка сообщений другим пользователям 
                if client != client_socket:
                    client.send(message)
            time.sleep(1)
            


myserver = Server('127.0.0.1', 5555) # Создание IP и Port
