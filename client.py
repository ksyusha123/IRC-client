import socket
import threading
import re


link_regex = re.compile(r'^((https)|(http)|(ftp))')


class IRCClient:
    def __init__(self, username, server, port=6667):
        self.username = username
        self.server = server
        self.port = port
        self.channel = ''
        self.conn = None
        self.connect()
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))
        self.send_nick()
        while True:
            resp = self.get_response()
            if "433" in resp:
                self.username = f"_{self.username}"
                self.send_nick()
            if "001" in resp:
                break

    def get_response(self):
        return self.conn.recv(512).decode("utf-8")

    def send_cmd(self, cmd, arg):
        self.conn.send(f"{cmd} {arg}\r\n".encode("utf-8"))

    def process_commands(self, cmd):
        if cmd.startswith('/'):
            command, arg = cmd.split()
            if command == '/join':
                self.channel = arg
            self.send_cmd(cmd.upper().replace('/', ''), arg)
        else:
            self.send_cmd("PRIVMSG", f"{self.channel} :{cmd}")

    def send_nick(self):
        self.send_cmd("NICK", self.username)
        self.send_cmd(
            "USER", f"{self.username} * * :{self.username}")

    def receive(self):
        while True:
            resp = self.get_response()
            print(resp)
            msg = resp.strip().split(":")
            if len(msg) < 3:
                continue
            second_part, message = self.parse_message(resp)
            yield f"<{second_part.split('!')[0]}> {message}"

    def parse_message(self, message):
        first_part = message[:message.find(':')]
        message = message[message.find(":")+1:]
        second_part = message[:message.find(':')]
        message = message[message.find(":") + 1:]
        return second_part, message

    def close(self):
        self.send_cmd("QUIT", "Good bye!")
