import socket
import threading
import re
import os


SERVER = "irc.libera.chat"
PORT = 6667


class Client:
    def __init__(self):
        self.nickname = 'ssoommm'
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((SERVER, PORT))
        # self.client_host_name = socket.gethostname()
        # self.client_username = os.environ.get('USERNAME')

        self.channel = '#libera'

        self.join_channel()
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def send_command(self, command, args):
        query = f"{command} {args}\r\n".encode("utf-8")
        self.conn.send(query)

    def send_message_to_channel(self, message):
        command = f"PRIVMSG {self.channel}"
        message = f":{message}"
        self.send_command(command, message)

    def receive(self):
        while True:
            response = self.conn.recv(1024).decode('utf-8')
            if "No Ident response" in response:
                self.send_command("NICK", self.nickname)
                self.send_command(
                    "USER", f"{self.nickname} * * :{self.nickname}"
                )
            if response == 'NICK':
                self.conn.send(self.nickname.encode('utf-8'))
            else:
                print(response)

    def write(self):
        while True:
            cmd = input(f"{self.nickname}: ")
            if cmd == "/quit":
                self.send_command("QUIT", "Good bye!")
            self.send_message_to_channel(cmd)

    def join_channel(self):
        cmd = "JOIN"
        self.send_command(cmd, self.channel)


client = Client()
