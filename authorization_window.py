from tkinter import *
from app import App
from client import IRCClient

client = IRCClient("python_task", "#python_task")


class AuthorizeWindow(Tk):
    def __init__(self):
        super().__init__()

        self.server_entry = Entry()
        self.server_entry.pack()
        self.server_entry_str = StringVar()
        self.server_entry_str.set('irc.libera.chat')
        self.server_entry["textvariable"] = self.server_entry_str

        self.nick_entry = Entry()
        self.nick_entry.pack()
        self.nick_entry_str = StringVar()
        self.nick_entry["textvariable"] = self.nick_entry_str

        self.button = Button(text="Enter", command=self.clicked)
        self.button.pack()

    def clicked(self):
        client.username = self.nick_entry_str.get()
        client.server = self.server_entry_str.get()
        self.destroy()
        App(client).mainloop()
