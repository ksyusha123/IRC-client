import sys
import os
from PyQt5.QtWidgets import QApplication
from authorization_window import AuthorizationWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = AuthorizationWindow()
    sys.exit(app.exec_())

