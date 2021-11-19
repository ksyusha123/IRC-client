import threading
import re
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, \
    QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QTextCursor

from link_parser import get_opengraph_tags
from file_saver import save_image, resize_image


link_regex = re.compile(r'((https)|(http)|(ftp)):\/{2}.*\/')


class ChatWindow(QWidget):
    def __init__(self, client):
        super(ChatWindow, self).__init__()
        self.setGeometry(200, 100, 1000, 500)
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
        output_field.setReadOnly(True)
        return output_field

    def send_data(self):
        cmd = self.input_field.text()
        self.client.process_commands(cmd)
        self.output_field.insertPlainText(f"<ME> {cmd}\n")

        link = re.search(link_regex, cmd)
        if link:
            self.show_og_tags(link)
        self.input_field.clear()

    def show_data(self):
        for received_message in self.client.receive():
            link = re.search(link_regex, received_message)
            if link:
                self.show_og_tags(link)
            self.output_field.insertPlainText(f"{received_message}\n")

    def show_og_tags(self, link):
        og_tags = get_opengraph_tags(link.group(0))
        if og_tags is not None:
            if 'site_name' in og_tags:
                self.output_field.insertPlainText(
                    f"{og_tags['site_name']}\n")
            if 'title' in og_tags:
                self.output_field.insertPlainText(
                    f"{og_tags['title']}\n")
            if 'image' in og_tags:
                self.show_image(og_tags["site_name"], og_tags["image"])

    def show_image(self, name, image):
        save_image(image, name)
        resize_image(name, self.width() // 2, self.height() // 2)
        document = self.output_field.document()
        cursor = QTextCursor(document)
        cursor.movePosition(QTextCursor.End)
        cursor.insertImage(f'{name}.jpg')
