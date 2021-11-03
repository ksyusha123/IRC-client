import socket
import threading


class IRCClient:
    def __init__(self, username, server, port=6667):
        self.username = username
        self.server = server
        self.port = port
        self.channel = '#python_task'
        self.conn = None
        self.connect()
        self.try_to_join_channel()
        write_thread = threading.Thread(target=self.process_commands)
        receive_thread = threading.Thread(target=self.receive)
        write_thread.start()
        receive_thread.start()

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))

    def get_response(self):
        return self.conn.recv(512).decode("utf-8")

    def send_cmd(self, cmd, message):
        command = f"{cmd} {message}\r\n".encode("utf-8")
        self.conn.send(command)

    def send_message_to_channel(self, message):
        command = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.send_cmd(command, message)

    def join_channel(self):
        cmd = "JOIN"
        channel = self.channel
        self.send_cmd(cmd, channel)

    def send_nick(self):
        self.send_cmd("NICK", self.username)
        self.send_cmd(
            "USER", f"{self.username} * * :{self.username}")

    def try_to_join_channel(self):
        joined = False
        while not joined:
            resp = self.get_response()
            print(resp.strip())
            if "No Ident response" in resp:
                self.send_nick()
            if "376" in resp:
                self.join_channel()
            if "433" in resp:
                self.username = f"_{self.username}"
                self.send_nick()
            if "PING" in resp:
                self.send_cmd("PONG", ":" + resp.split(":")[1])
            if "366" in resp:
                joined = True

    def process_commands(self):
        while True:
            cmd = input(f"<{self.username}> ").strip()
            if cmd == "/quit":
                self.send_cmd("QUIT", "Good bye!")
                # self.conn.close()
                break
            self.send_message_to_channel(cmd)

    def receive(self):
        while True:
            resp = self.get_response()
            msg = resp.strip().split(":")
            if len(msg) < 3:
                continue
            yield f"<{msg[1].split('!')[0]}> {msg[2].strip()}"

    def close(self):
        self.send_cmd("QUIT", "Good bye!")

# import socket
# import threading
#
#
# class IRCClient:
#     def __init__(self, username, server="irc.libera.chat", port=6667):
#         self.username = username
#         self.server = server
#         self.port = port
#         self.channel = '#python_task'
#         self.conn = None
#         self.connect()
#         receive_thread = threading.Thread(target=self.receive)
#         receive_thread.start()
#
#     def connect(self):
#         self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.conn.connect((self.server, self.port))
#
#     def get_response(self):
#         return self.conn.recv(512).decode("utf-8")
#
#     def send_cmd(self, *args):
#         cmd = args[0]
#         arg = args[1]
#         if cmd == 'PRIVMSG':
#             arg = f':{arg}'
#             cmd += f' {self.channel}'
#         if cmd == 'JOIN':
#             self.channel = arg
#         command = f"{cmd} {arg}\r\n".encode("utf-8")
#         self.conn.send(command)
#
#     def join_channel(self, channel):
#         cmd = "JOIN"
#         self.send_cmd(cmd, channel)
#
#     def send_nick(self):
#         self.send_cmd("NICK", self.username)
#         self.send_cmd(
#             "USER", f"{self.username} * * :{self.username}")
#
#     def receive(self):
#         while True:
#             resp = self.get_response()
#             if "No Ident response" in resp:
#                 self.send_nick()
#             if "376" in resp:
#                 self.send_cmd("JOIN", self.channel)
#             if "433" in resp:
#                 self.username = f"_{self.username}"
#                 self.send_nick()
#             if "PING" in resp:
#                 self.send_cmd("PONG", ":" + resp.split(":")[1])
#             msg = resp.strip().split(":")
#             if len(msg) < 3:
#                 continue
#             yield f"<{msg[1].split('!')[0]}> {msg[2].strip()}"
