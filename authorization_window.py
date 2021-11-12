from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, \
    QLineEdit

from client import IRCClient
from chat_window import ChatWindow


class AuthorizationWindow(QWidget):
    def __init__(self):
        super(AuthorizationWindow, self).__init__()
        self.setWindowTitle('Authorization')
        # self.setGeometry(300, 300, 310, 200)

        grid = QGridLayout()
        self.setLayout(grid)
        nick_label = QLabel('Enter your nickname')
        self.nick_input = QLineEdit()
        self.nick_input.setFocus()
        server_name_label = QLabel('Enter server name')
        self.server_name_input = QLineEdit()
        self.server_name_input.insert("irc.libera.chat")
        button = QPushButton('Enter')
        grid.addWidget(nick_label, 1, 1)
        grid.addWidget(self.nick_input, 2, 1)
        grid.addWidget(server_name_label, 3, 1)
        grid.addWidget(self.server_name_input, 4, 1)
        grid.addWidget(button, 5, 1)
        button.clicked.connect(self.clicked)

        self.show()

    def clicked(self):
        client = IRCClient(self.nick_input.text(), self.server_name_input.text())
        self.hide()
        self.chat = ChatWindow(client)
