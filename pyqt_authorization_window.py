import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QTextBrowser, QTextEdit, QPushButton, QLineEdit


class ChatWindow(QWidget):
    def __init__(self):
        super(ChatWindow, self).__init__()

        grid = QGridLayout()
        self.setLayout(grid)
        messages_label = QLabel('Messages')
        self.output_window = QTextBrowser()
        grid.addWidget(messages_label, 1, 2)
        grid.addWidget(self.output_window, 2, 1, 2, 3)
        self.input_window = QTextEdit()
        self.enter_button = QPushButton('Enter')
        grid.addWidget(self.input_window, 4, 1, 4, 2)
        grid.addWidget(self.enter_button, 4, 3, 6, 3)

        self.show()


class AuthorizationWindow(QWidget):
    def __init__(self, client=None):
        super(AuthorizationWindow, self).__init__()
        self.client = client
        self.setWindowTitle('Authorization')
        self.setGeometry(300, 300, 310, 200)

        grid = QGridLayout()
        self.setLayout(grid)
        nick_label = QLabel('Enter your nickname')
        self.nick_input = QLineEdit()
        server_name_label = QLabel('Enter server name')
        self.server_name_input = QLineEdit()
        button = QPushButton('Enter')
        grid.addWidget(nick_label, 1, 1)
        grid.addWidget(self.nick_input, 2, 1)
        grid.addWidget(server_name_label, 3, 1)
        grid.addWidget(self.server_name_input, 4, 1)
        grid.addWidget(button, 5, 1)
        button.clicked.connect(self.clicked)

        self.show()

    def clicked(self):
        # self.client.nick = self.nick_input.text()
        # self.client.server_name = self.server_name_input.text()
        self.hide()
        self.chat_window = ChatWindow()


app = QApplication(sys.argv)
a = AuthorizationWindow()

sys.exit(app.exec_())
# у клиента должны быть следующие поля: nick, server_name
