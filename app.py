from tkinter import *
from tkinter import scrolledtext
import threading


class App(Tk):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.entry = Entry()
        self.entry.pack()
        self.message = StringVar()
        self.message.set("hi")
        self.entry["textvariable"] = self.message
        self.entry.bind('<Key-Return>', self.send_user_data)
        self.chat_box = scrolledtext.ScrolledText()
        self.chat_box.pack()

        get_messages_thread = threading.Thread(target=self.get_chat_messages)
        get_messages_thread.start()

    def send_user_data(self):
        self.client.send_message_to_channel(self.message.get())
        self.chat_box.insert(INSERT, f"<ME> {self.message.get()}\n")
        self.message.set("")

    def get_chat_messages(self):
        for received_message in self.client.receive():
            self.chat_box.insert(INSERT, f"{received_message}\n")


