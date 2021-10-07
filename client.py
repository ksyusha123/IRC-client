import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input('IP-адрес сервера: ')
name = input('Nickname: ')
port = 9090
client.connect((host, port))
print('-' * 5 + f"Подключился к серверу {host}" + '-' * 5)
print('-' * 5 + 'Enter, чтобы закрыть соединение с сервером' + '-' * 5)


def send():
    while True:
        message = input('Me: ')
        if message == 'enter':
            break
        client.send(f'{name}: {message}'.encode('utf-8'))


def receive():
    while True:
        message = client.recv(1024)
        print(message.decode('utf-8'))


input_thread = threading.Thread(target=receive, name='input')
output_thread = threading.Thread(target=send, name='out')

input_thread.start()
output_thread.start()

input_thread.join()
output_thread.join()

print('-' * 5 + 'сервер отключен' + '-' * 5)
client.close()
