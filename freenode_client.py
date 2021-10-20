import socket
import threading
import sys
import click
import time


# def channel(channel):
#     if channel.startswith("#") == False:
#         return "#" + channel
#     return channel

# def print_response(client):
#


class IRCClient:
    def __init__(self, username, channel, server="irc.libera.chat", port=6667):
        self.username = username
        self.server = server
        self.port = port
        self.channel = channel
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
        cmd = input(f"<{self.username}> ").strip()
        while cmd != "/quit":
            self.send_message_to_channel(cmd)
            cmd = input(f"<{self.username}> ").strip()
        self.send_cmd("QUIT", "Good bye!")

    def receive(self):
        resp = self.get_response()
        while resp:
            msg = resp.strip().split(":")
            if len(msg) < 3:
                continue
            print(f"<{msg[1].split('!')[0]}> {msg[2].strip()}")


@click.command()
@click.argument('username')
@click.argument('channel')
def main(username, channel):
    client = IRCClient(username, channel)
    # while (cmd != "/quit"):
    #     cmd = input("< {}> ".format(username)).strip()
    #     if cmd == "/quit":
    #         client.send_cmd("QUIT", "Good bye!")
    #     client.send_message_to_channel(cmd)
    #
    #     # socket conn.receive blocks the program until a response is received
    #     # to prevent blocking program execution, receive should be threaded
    #     response_thread = threading.Thread(target=print_response)
    #     response_thread.daemon = True
    #     response_thread.start()


if __name__ == "__main__":
    main()
