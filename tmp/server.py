import socket


pairs = []


def server_program():
    host = '172.20.10.5'
    port = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        pairs.append((conn, address))
        for pair in pairs:
            data = pair[0].recv(1024).decode()
            if not data:
                break
            print("from connected user: " + str(data))
            data = input(' -> ')
            for pair1 in pairs:
                pair1[1].send(data.encode())
        conn.close()


if __name__ == '__main__':
    server_program()
