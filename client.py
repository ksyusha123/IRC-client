import socket
import threading
import re
import os


class Client:
    def __init__(self):
        print('Enter your nick name (of a-z, A-Z, 0-9 symbols)')
        self.nickname = input("My nickname: ")
        nick_reg = re.compile(r'[a-zA-Z0-9]{1,9}')
        f = nick_reg.match(self.nickname) is None
        while f:
            print('Nickname is invalid, enter another')
            self.nickname = input("My nickname: ")
            f = nick_reg.match(self.nickname) is None

        print('Enter server\'s ip-address')
        self.server_ip = input('Server ip: ')
        print('Enter port')
        self.port = int(input('Port: '))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server_ip, self.port))
        self.client_host_name = socket.gethostname()
        self.client_username = os.environ.get('USERNAME')

        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
            except:
                print("An error occured!")
                self.client.close()
                break

    def write(self):
        while True:
            message = '{}: {}'.format(self.nickname, input(''))
            self.client.send(message.encode('ascii'))
