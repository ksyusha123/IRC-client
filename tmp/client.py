import socket

sock = socket.socket()
sock.connect(('192.168.56.1', 9090))
sock.send(bytes(input().encode('utf-8')))

data = sock.recv(1024)
sock.close()
print('wait')
print(data.decode('utf-8'))
