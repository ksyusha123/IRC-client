from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QTextEdit, \
    QPushButton


class ChatWindow(QWidget):
    def __init__(self, client):
        super(ChatWindow, self).__init__()

        self.client = client

        grid = QGridLayout()
        self.setLayout(grid)
        messages_label = QLabel('Messages')
        self.output_window = QTextEdit()
        grid.addWidget(messages_label, 1, 2)
        grid.addWidget(self.output_window, 2, 1, 2, 3)
        self.input_window = QTextEdit()
        self.enter_button = QPushButton('Enter')
        self.enter_button.clicked.connect(self.send_data)
        grid.addWidget(self.input_window, 4, 1, 4, 2)
        grid.addWidget(self.enter_button, 4, 3, 6, 3)

        show_data_thread = threading.Thread(target=self.show_data)
        show_data_thread.start()

        self.show()

    def send_data(self):
        cmd = self.input_window.toPlainText()
        self.client.send_message_to_channel(cmd)
        self.output_window.insertPlainText(f"<ME> {cmd}\n")
        self.input_window.clear()

    def show_data(self):
        for received_message in self.client.receive():
            self.output_window.insertPlainText(f"{received_message}\n")


