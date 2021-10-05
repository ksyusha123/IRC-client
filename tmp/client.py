import socket
import threading


def read_sok(sor):
    while 1:
        data = sor.recv(1024)
        print(data.decode('utf-8'))


def client():
    server = '127.0.0.1', 9090  # Данные сервера
    alias = input()  # Вводим наш псевдоним
    sor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sor.bind(('', 0))  # Задаем сокет как клиент
    sor.sendto((alias + ' Connect to server').encode('utf-8'), server)  # Уведомляем сервер о подключении
    potok = threading.Thread(target=read_sok(sor))
    potok.start()
    print('client ready')
    while 1:
        mensahe = input()
        sor.sendto(('[' + alias + ']' + mensahe).encode('utf-8'), server)


client()