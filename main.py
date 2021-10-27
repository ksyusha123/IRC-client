from tkinter import *
from tkinter import scrolledtext
from client import IRCClient

import threading


client = IRCClient("python_task", "#python_task")


class App(Frame):
    def __init__(self, window):
        super().__init__(window)

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

        window.mainloop()

    def send_user_data(self, event):
        client.send_message_to_channel(self.message.get())
        self.chat_box.insert(INSERT, f"ME: {self.message.get()}\n")
        self.message.set("")

    def get_chat_messages(self):
        for received_message in client.receive():
            self.chat_box.insert(INSERT, f"{received_message}\n")


window = Tk()
app = App(window)
app.mainloop()

