import socket

while True:
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()
    print('connected to ' + str(addr))

    data = conn.recv(1024)
    conn.send(data.upper())
conn.close()