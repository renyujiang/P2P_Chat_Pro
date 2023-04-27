import datetime
import json
import os
import queue
import socket
import sys
import threading
from time import sleep

import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QTextCursor
from PyQt5.QtWidgets import QFileDialog

quit_queue = queue.Queue()
server_ip = 'http://127.0.0.1:10000'
path = ''
username = 'Default User'


class P2P_Chat_Comm(QtWidgets.QMainWindow):
    def __init__(self, mode, connection):
        super(P2P_Chat_Comm, self).__init__()

        # Load the UI file
        uic.loadUi(path + '/GUI/comm.ui', self)

        # set mode for window
        self.mode = mode
        self.connection = connection

        # formats for chat display
        self.format_user = QTextCharFormat()
        font_user = QFont()
        font_user.setBold(True)
        font_user.setPointSize(16)
        self.format_user.setForeground(QColor("black"))
        self.format_user.setFont(font_user)

        self.format_msg = QTextCharFormat()
        color_msg_bg = QColor("grey")
        color_msg_bg.setAlphaF(0.2)
        self.format_msg.setBackground(color_msg_bg)

        self.format_me = QTextCharFormat()
        font_me = QFont()
        font_me.setBold(True)
        color_me = QColor("blue")
        self.format_me.setForeground(color_me)
        self.format_me.setFont(font_me)

        # Connect signal/slot
        self.sendButton.clicked.connect(self.sendButton_clicked)
        self.quitButton.clicked.connect(self.quitButton_clicked)
        self.clearButton.clicked.connect(self.clearButton_clicked)
        self.fileButton.clicked.connect(self.fileButton_clicked)

        # Start a new thread to handle server communication
        t = threading.Thread(target=self.receive_message, args=(self.connection, (ip, port)))
        t.start()

    def sendButton_clicked(self):
        # Handle button click event
        message = self.userInput.toPlainText()
        print('send message: ' + message)
        self.updateDisplay_msg('Me', message)

        # Send message to the server
        self.connection.sendall(message.encode())
        self.userInput.clear()

    def quitButton_clicked(self):
        message = 'this_is_to_close_connection'
        print('close connection')
        self.updateDisplay_msg('System', 'Connection closed, windows automatically close in three seconds')
        sleep(3)
        # os._exit(0)

    def clearButton_clicked(self):
        self.chatDisplay.clear()
        self.userInput.clear()

    def fileButton_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            caption='Open File', filter='All Files (*.*)')
        if file_path:
            url = server_ip + '/upload'

            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'username': username}
                response = requests.post(url, files=files, data=data)

            if response.ok:
                content = response.content.decode('utf-8')
                # decode the content from json to list
                data = json.loads(content)
                print('File uploaded successfully')
                file_url = server_ip + '/share/' + username + '/' + data['filename']
                self.updateDisplay_msg('Me', file_url)
                # Send message to the server
                self.connection.sendall(file_url.encode())
            else:
                self.updateDisplay_msg('Sys', 'Error uploading file')
                print('Error uploading file')
        else:
            self.updateDisplay_msg('Sys', 'No file selected')

    def updateDisplay_msg(self, who: str, message: str):
        cursor = self.chatDisplay.textCursor()
        cursor.movePosition(QTextCursor.End)
        if who == 'Me':
            cursor.insertText('\n' + who + ': \n', self.format_me)
        else:
            cursor.insertText('\n' + who + ': \n', self.format_user)
        cursor.insertText(message, self.format_msg)

        self.chatDisplay.verticalScrollBar().setValue(self.chatDisplay.verticalScrollBar().maximum())

    def receive_message(self, conn, addr):
        try:
            while True:
                # Receive message from the other side
                data = conn.recv(1024)

                if not data:
                    # If the other side closes the connection, break the loop
                    break

                if data.decode() == 'this_is_to_close_connection':
                    quit_queue.put('this_is_to_close_connection')
                    self.updateDisplay_msg("System", "Connection closed")
                    self.sendButton.setEnabled(False)
                    self.quitButton.setEnabled(False)
                    break

                # Print the message received from the other side
                print(f"Message from {addr[0]}:{addr[1]}: {data.decode()}")
                self.updateDisplay_msg(username, data.decode())

            # Close the socket connection
            conn.close()
        except Exception as e:
            print('connection closed')
            return e


def server(ip_listen, port_listen):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind IP address and port number
    s.bind((ip_listen, port_listen))

    # Listen on the port and wait for connections
    s.listen(1)
    print(f"Listening on port {port_listen}...")

    # Wait for a client connection
    conn, addr = s.accept()
    print(f"Connected to client {addr[0]}:{addr[1]}")

    return conn


def client(ip_connect, port_connect):
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect((ip_connect, port_connect))

    return sock


def txt_log_function(msg):
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("comm_GUI_record.txt", mode="a", encoding="utf-8") as file:
        file.write("\n" + formatted_datetime + ": " + msg)


# def get_hyper_link(url):
#     return f'<a href="{url}" style="color:#ffb61e;font-size:20px;font-family:Microsoft YaHei"><b>{url}</b></a>'


if __name__ == '__main__':

    # Get command line arguments
    if len(sys.argv) != 6:
        print("Usage: python communication.py <server/client> <ip> <port> <path> <username>")
        txt_log_function("Arguments error")
        sys.exit()

    mode = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])
    path = sys.argv[4]
    username = sys.argv[5]

    txt_log_function("Mode: " + mode + ", IP: " + ip + ", Port: " + str(port))

    app = QtWidgets.QApplication(sys.argv)

    if mode == "server":
        connection_server = server(ip, port)
        window = P2P_Chat_Comm(mode=0, connection=connection_server)
        print(connection_server)
        txt_log_function("Server connection established")
        # connection_server.close()
    elif mode == "client":
        connection_client = client(ip, port)
        window = P2P_Chat_Comm(mode=1, connection=connection_client)
        print(connection_client)
        txt_log_function("Client connection established")
        # connection_client.close()
    else:
        print("Invalid mode, please use 'server' or 'client'")
        txt_log_function("Invalid mode, please use 'server' or 'client'")
        sys.exit()

    window.show()
    sys.exit(app.exec_())
