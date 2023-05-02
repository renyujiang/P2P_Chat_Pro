import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QColor
from applescript import tell

server_ip = '127.0.0.1'


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.resize(400, 200)
        self.setup_ui()

    def setup_ui(self):
        # Username label and line edit
        self.username_label = QLabel('Username:', self)
        self.username_line_edit = QLineEdit(self)
        self.username_line_edit.setFixedSize(225, 25)
        self.set_large_font([self.username_label, self.username_line_edit])
        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_line_edit)
        username_layout.setSpacing(0)  # Set the spacing value

        # Password label and line edit
        self.password_label = QLabel('Password:', self)
        self.password_line_edit = QLineEdit(self)
        self.password_line_edit.setEchoMode(QLineEdit.Password)
        self.password_line_edit.setFixedSize(225, 25)
        self.set_large_font([self.password_label, self.password_line_edit])
        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_line_edit)
        password_layout.setSpacing(0)  # Set the spacing value

        # Error message label
        self.error_label = QLabel('Welcome to use P2P Pro', self)
        self.error_label.setStyleSheet('color: blue')
        error_layout = QHBoxLayout()
        error_layout.addStretch(1)  # Add a stretchable space on the left
        error_layout.addWidget(self.error_label)
        error_layout.addStretch(1)  # Add a stretchable space on the right

        # Add margin at the bottom
        error_layout.setContentsMargins(0, 0, 0, 0)

        # Login and register buttons
        self.login_button = QPushButton('Login', self)
        self.login_button.setFixedSize(125, 45)
        self.login_button.clicked.connect(self.login)
        self.register_button = QPushButton('Register', self)
        self.register_button.setFixedSize(125, 45)
        self.register_button.clicked.connect(self.register)
        self.set_large_font([self.login_button, self.register_button])

        # Horizontal layout for the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        # Vertical layout
        vbox = QVBoxLayout()
        vbox.addLayout(username_layout)
        vbox.addLayout(password_layout)
        vbox.addLayout(error_layout)
        vbox.addLayout(button_layout)
        self.setLayout(vbox)

    def login(self):
        try:

            username = self.username_line_edit.text()
            password = self.password_line_edit.text()

            import requests

            url = 'http://' + server_ip + ':10000/login'
            params = {'username': username, 'password': password}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                if response.content.decode('utf-8') == 'Success':
                    self.error_label.setText('Login succeeded')
                    self.error_label.setStyleSheet('color: green')
                    # Get the absolute path of the current file
                    current_file = os.path.abspath(__file__)

                    # Get the absolute path of the directory containing the current file
                    current_dir = os.path.dirname(current_file)

                    cmd = 'cd ' + current_dir + '\n '
                    cmd += 'python ' + 'console_GUI.py ' + username
                    tell.app('Terminal', 'do script "' + cmd + '"')
                    exit(0)
                else:
                    self.error_label.setText('Your username or password is wrong')
                    self.error_label.setStyleSheet('color: red')
            else:
                print(f'Login failed: {response.status_code}')
        except Exception as e:
            print(f'Login failed: {e}')
            self.error_label.setText(str(e))

    def register(self):
        try:

            username = self.username_line_edit.text()
            password = self.password_line_edit.text()

            import requests

            url = 'http://' + server_ip + ':10000/register'
            params = {'username': username, 'password': password}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                if response.content.decode('utf-8') == 'Success':
                    self.error_label.setText('Register succeeded')
                    self.error_label.setStyleSheet('color: green')
                else:
                    self.error_label.setText('Register failed')
                    self.error_label.setStyleSheet('color: red')
            else:
                print(f'Login failed: {response.status_code}')
        except Exception as e:
            print(f'Login failed: {e}')
            self.error_label.setText(str(e))

    def set_large_font(self, widgets):
        font = QFont()
        font.setPointSize(18)
        for widget in widgets:
            widget.setFont(font)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
