import threading
import re
import requests
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, \
    QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QTextCursor

from link_parser import get_opengraph_tags


link_regex = re.compile(r'^((https)|(http)|(fttp))')


class ChatWindow(QWidget):
    def __init__(self, client):
        super(ChatWindow, self).__init__()
        self.client = client
        self.output_field = self.create_output_field()
        self.input_field = self.create_input_field()
        self.enter_button = QPushButton('Enter')
        self.enter_button.clicked.connect(self.send_data)

        self.init_layout()

        show_data_thread = threading.Thread(target=self.show_data)
        show_data_thread.start()

        self.show()

    def init_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Messages"))
        layout.addWidget(self.output_field)
        layout.addLayout(self.create_input_field_layout())
        self.setLayout(layout)

    def create_input_field_layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.input_field)
        layout.addWidget(self.enter_button)
        return layout

    def create_input_field(self):
        input_field = QLineEdit()
        input_field.returnPressed.connect(self.send_data)
        input_field.setFocus()
        return input_field

    def create_output_field(self):
        output_field = QTextEdit()
        output_field.setOpenExternalLinks(True)
        output_field.setReadOnly(True)
        return output_field

    def send_data(self):
        cmd = self.input_field.text()
        if re.search(link_regex, cmd):
            og_tags = get_opengraph_tags(cmd)
            self.output_field.insertPlainText(f"{og_tags['site_name']}\n")
            self.output_field.insertPlainText(f"{og_tags['title']}\n")
            self.show_image(og_tags["site_name"], og_tags["image"])
        self.client.process_commands(cmd)
        self.output_field.insertPlainText(f"<ME> {cmd}\n")
        self.input_field.clear()

    def show_data(self):
        for received_message in self.client.receive():
            self.output_field.insertPlainText(f"{received_message}\n")

    def show_image(self, name, image):
        save_image(image, name)
        document = self.output_field.document()
        cursor = QTextCursor(document)
        cursor.movePosition(QTextCursor.End)
        cursor.insertImage('tmp.jpg')


def save_image(link, name):
    image_data = requests.get(link).content
    with open('tmp.jpg', 'wb') as f:
        f.write(image_data)
