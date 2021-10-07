import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.43.32'
port = 9090
server.bind((host, port))
server.listen(5)
print('Press Enter to leave the server')

clients = list()
end = list()


def accept():
    while True:
        client, address = server.accept()
        clients.append(client)
        print(f"Сервер подключен через {address}: "
              f"текущее количество подключений: "
              f"{len (clients)}")


def receive_data(client):
    while True:
        try:
            client_input = client.recv(1024)
        except Exception as e:
            clients.remove(client)
            end.remove(client)
            print(f"Клиент отключен:"
                  f" текущее количество подключений:"
                  f"{len (clients)}")
            break
        print(client_input.decode('utf-8'))
        for other_client in clients:
            if other_client != client:
                other_client.send(client_input)


def send_data():
    while True:
        message_to_send = input()
        if message_to_send == 'enter':
            break
        print(f"Отправить всем: {message_to_send}")
    for client in clients:
        print(client)
        client.send(f"Сервер: {message_to_send}".encode('utf-8)'))


def init_threads():
    while True:
        for client in clients:
            if client in end:
                continue
            index = threading.Thread(target=receive_data, args=(client,))
            index.start()
            end.append(client)


input_thread = threading.Thread(target=init_threads, name='input')
input_thread.start()

output_thread = threading.Thread(target=send_data, name='out')
output_thread.start()

accept_thread = threading.Thread(target=accept, name='accept')
accept_thread.start()

input_thread.join()
output_thread.join()

for client in clients:
    client.close()
print('-' * 5 + 'сервер отключен' + '-' * 5)
