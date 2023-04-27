import ast
import datetime
import json
import os
import queue
import random
import socket
import sys
import threading
from time import sleep

import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QTextCharFormat, QColor, QFont
from applescript import tell

import sqlite_op

quit_queue = queue.Queue()

my_info = {'id': 0, 'name': 'Default User', 'ip': '127.0.0.1'}
if len(sys.argv) == 2:
    my_info['name'] = sys.argv[1]

server_ip = 'http://127.0.0.1:10000'
test_ip = "127.0.0.1"

# listen to the port
listen_port = 8080


class P2P_Chat_Console(QtWidgets.QMainWindow):
    def __init__(self):
        super(P2P_Chat_Console, self).__init__()

        # Load the UI file
        uic.loadUi('./GUI/console.ui', self)

        # some global variables
        self.online = False
        self.locked = False
        self.listen_thread_input_queue = queue.Queue()
        self.listen_thread_input_sign = queue.Queue()

        # Connect signal/slot
        self.commandButton.clicked.connect(self.commandButton_clicked)
        self.listOnlineButton.clicked.connect(self.listOnlineButton_clicked)
        self.connectButton.clicked.connect(self.connectButton_clicked)
        self.onlineButton.clicked.connect(self.onlineButton_clicked)
        self.myCloudStorageButton.clicked.connect(self.myCloudStorageButton_clicked)
        self.lockButton.clicked.connect(self.lockButton_clicked)
        self.quitButton.clicked.connect(self.quitButton_clicked)

        # formats for chat display

        self.format_default = QTextCharFormat()
        font_default = QFont()
        font_default.setBold(False)
        font_default.setPointSize(16)
        self.format_default.setForeground(QColor("black"))
        self.format_default.setFont(font_default)

        self.format_bold = QTextCharFormat()
        font_bold = QFont()
        font_bold.setBold(True)
        font_bold.setPointSize(16)
        self.format_bold.setForeground(QColor("black"))
        self.format_bold.setFont(font_bold)

        self.format_green = QTextCharFormat()
        font_green = QFont()
        font_green.setBold(True)
        font_green.setPointSize(16)
        self.format_green.setForeground(QColor("green"))
        self.format_green.setFont(font_green)

        self.format_light_blue = QTextCharFormat()
        font_light_blue = QFont()
        font_light_blue.setBold(True)
        font_light_blue.setPointSize(16)
        self.format_light_blue.setForeground(QColor("#3498DB"))
        self.format_light_blue.setFont(font_light_blue)

        self.format_red = QTextCharFormat()
        font_red = QFont()
        font_red.setBold(True)
        font_red.setPointSize(16)
        self.format_red.setForeground(QColor("red"))
        self.format_red.setFont(font_red)

        listen_thread_console = threading.Thread(target=self.listen_thread)
        listen_thread_console.setDaemon(True)
        listen_thread_console.start()
        sleep(1)

        self.updateDisplay("\nHi, " + my_info['name'] + "\nWelcome to P2P PRO Chat Console\n",
                           format_msg=self.format_bold)

    # command button clicked
    def commandButton_clicked(self):
        print('command button clicked')
        # self.updateDisplay('\ncommand button clicked')
        input_text = self.input.text()
        if not self.listen_thread_input_sign.empty():
            self.listen_thread_input_queue.put(input_text)
            self.updateDisplay('\n' + input_text, format_msg=self.format_light_blue)
        else:
            self.updateDisplay('Unknown command: ' + input_text, format_msg=self.format_red)

    # list online button clicked
    def listOnlineButton_clicked(self):
        try:
            print('list online button clicked')
            self.updateDisplay('\nOnline Clients:', format_msg=self.format_bold)
            url = server_ip + '/online'
            response = requests.get(url)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                print(content)
                if content == '[]':
                    self.updateDisplay('\n' + "No online client", format_msg=self.format_light_blue)
                my_list = ast.literal_eval(content)
                my_tuples = [tuple(x) for x in my_list]
                for i in range(len(my_tuples)):
                    self.updateDisplay('\n' + str(my_tuples[i][0]) + '\t' + str(my_tuples[i][1]), format_msg=self.
                                       format_light_blue)
            else:
                print("Error: " + str(response.status_code))
                self.updateDisplay('\n' + "Error: " + str(response.status_code))
        except Exception as e:
            print(e)
            self.updateDisplay('\n' + str(e))

    # Connect button clicked
    def connectButton_clicked(self):
        print('connect button clicked')
        # self.updateDisplay('\nconnect button clicked')
        try:
            ip_to_connect = self.input.text()
            print(ip_to_connect)
            self.connect_to_client(ip_to_connect)
        except Exception as e:
            print(e)
            self.updateDisplay('\n' + str(e))

    # Online button clicked
    def onlineButton_clicked(self):
        try:
            print('online button clicked')
            if self.online is True:
                self.online = False
                self.onlineButton.setText("Offline")
                self.onlineButton.setStyleSheet("QPushButton {background-color: qlineargradient(spread:pad, x1:0, "
                                                "y1:1, x2:0.6, y2:0.6, stop:0 white, stop:1 red); border-radius: "
                                                "10px;color: white;font:bold;}")

                self.updateDisplay('\n' + "You are now Offline", format_msg=self.format_red)
                url = server_ip + '/delete_client'
                params = {'username': my_info['name']}
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    pass
                else:
                    self.updateDisplay('\n' + "Error: " + str(response.status_code))
            else:
                self.online = True
                self.onlineButton.setText("Online")
                self.onlineButton.setStyleSheet("QPushButton {background-color: qlineargradient(spread:pad, x1:0, "
                                                "y1:1, x2:0.6, y2:0.6, stop:0 white, stop:1 green); border-radius: "
                                                "10px;color: white;font:bold;}")

                self.updateDisplay('\n' + "You are now Online", format_msg=self.format_green)
                url = server_ip + '/add_client'
                params = {'username': my_info['name'], 'ip_addr': my_info['ip']}
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    pass
                else:
                    self.updateDisplay('\n' + "Error: " + str(response.status_code))
                # self.onlineButton.setBackgroundColor(QColor("green"))
        except Exception as e:
            print(e)
            self.updateDisplay('\n' + str(e))

    # My cloud storage button clicked
    def myCloudStorageButton_clicked(self):
        print('my cloud storage button clicked')
        # self.updateDisplay('\nmy cloud storage button clicked')
        self.updateDisplay('\nMy Cloud Storage:', format_msg=self.format_bold)
        try:
            url = server_ip + '/storage'
            params = {'username': my_info['name']}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                # decode the content from json to list
                data = json.loads(content)
                if data['files'] == []:
                    self.updateDisplay('\n' + "No file in your cloud storage", format_msg=self.format_light_blue)
                for i in data['files']:
                    print(i)
                    self.updateDisplay('\n' + i, format_msg=self.format_light_blue)
            else:
                print("Error: " + str(response.status_code))
                self.updateDisplay('\n' + "Error: " + str(response.status_code))
        except Exception as e:
            print(e)
            self.updateDisplay('\n' + str(e))

    # Quit button clicked
    def quitButton_clicked(self):
        print('quit button clicked')
        self.updateDisplay("Console window will automatically close in three seconds", format_msg=self.format_bold)
        sleep(3)
        os._exit(0)

    # Lock button clicked
    def lockButton_clicked(self):
        print('lock button clicked')
        # self.updateDisplay('\nlock button clicked')
        if self.locked is True:
            self.locked = False
            self.lockButton.setStyleSheet("QPushButton {background-color: #D7DBDD; border-radius: 10px;color: green;}")
            self.lockButton.setText("Unlocked")
            self.input.setEnabled(True)
            self.connectButton.setEnabled(True)
            self.listOnlineButton.setEnabled(True)
            self.commandButton.setEnabled(True)
            self.onlineButton.setEnabled(True)
            self.myCloudStorageButton.setEnabled(True)
            self.quitButton.setEnabled(True)
            self.updateDisplay('\n' + "You are now unlocked", format_msg=self.format_green)
        else:
            self.locked = True
            self.lockButton.setStyleSheet("QPushButton {background-color: #D7DBDD; border-radius: 10px;color: red;}")
            self.lockButton.setText("Locked")
            self.input.setEnabled(False)
            self.connectButton.setEnabled(False)
            self.listOnlineButton.setEnabled(False)
            self.commandButton.setEnabled(False)
            self.onlineButton.setEnabled(False)
            self.myCloudStorageButton.setEnabled(False)
            self.quitButton.setEnabled(False)
            self.updateDisplay('\n' + "You are now locked", format_msg=self.format_red)

    # connect to a client
    def connect_to_client(self, client_ip):
        # get local ip address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # use the port that the server is listening on
        server_address = (client_ip, listen_port)
        print('connecting to %s port %s' % server_address)
        self.updateDisplay('\n' + 'connecting to %s port %s' % server_address, format_msg=self.format_bold)
        # send a connection request to the server
        sock.connect(server_address)
        # receive a confirmation message from the server
        message = sock.recv(1024).decode()
        message_split = message.split()
        if message_split[0] == 'confirm':
            # create two threads to send and receive messages
            print("\x1b[1A\x1b[2K", end="")
            print('Connection established')
            now = datetime.datetime.now()
            date_string = now.strftime("%m, %d, %Y")
            username1 = 'this client'
            ip_addr1 = ip_address
            username2 = 'unknown'
            ip_addr2 = client_ip
            # sqlite_op.insert_history_connections(date_string, username1, ip_addr1, username2, ip_addr2,
            #                                      'active, success')
            self.new_terminal_client(client_ip, message_split[1])
            # print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
            return True
        elif message_split[0] == 'reject':
            print("\x1b[1A\x1b[2K", end="")
            print('Connection rejected')
            now = datetime.datetime.now()
            date_string = now.strftime("%m, %d, %Y")
            username1 = 'this client'
            ip_addr1 = ip_address
            username2 = 'unknown'
            ip_addr2 = client_ip
            sqlite_op.insert_history_connections(date_string, username1, ip_addr1, username2, ip_addr2,
                                                 'active, failure')
            # print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
            return False
        else:
            print("\x1b[1A\x1b[2K", end="")
            print('Unknown message, connection closed')
            now = datetime.datetime.now()
            date_string = now.strftime("%m, %d, %Y")
            username1 = 'this client'
            ip_addr1 = ip_address
            username2 = 'unknown'
            ip_addr2 = client_ip
            sqlite_op.insert_history_connections(date_string, username1, ip_addr1, username2, ip_addr2,
                                                 'active, failure')
            # print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
            return False

    # open new terminal for server
    def new_terminal_server(self, ip, port):
        print("open new server terminal, parameters = " + ip + ", " + str(port))
        # Get the absolute path of the current file
        current_file = os.path.abspath(__file__)

        # Get the absolute path of the directory containing the current file
        current_dir = os.path.dirname(current_file)

        cmd = 'python ' + current_dir + '/comm_GUI.py ' + 'server ' + ip + ' ' + str(port)+' '+current_dir+' '+my_info['name']

        tell.app('Terminal', 'do script "' + cmd + '"')

    # open new terminal for client
    def new_terminal_client(self, ip, port):
        sleep(3)
        print("open new client terminal, parameters = " + ip + ", " + str(port))
        # Get the absolute path of the current file
        current_file = os.path.abspath(__file__)

        # Get the absolute path of the directory containing the current file
        current_dir = os.path.dirname(current_file)

        cmd = 'python ' + current_dir + '/comm_GUI.py ' + 'client ' + ip + ' ' + str(port)+' '+current_dir+' '+my_info['name']

        tell.app('Terminal', 'do script "' + cmd + '"')

    # listen thread's function
    def listen_thread(self):
        # get local ip address
        hostname = socket.gethostname()
        # ip_address = socket.gethostbyname(hostname)

        # this is for testing, comment out when using on different computers
        ip_address = test_ip

        my_info['ip'] = ip_address
        print("Local IP address: " + ip_address)
        # self.updateDisplay("Local IP address: " + ip_address, format_msg=self.format_bold)
        # create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the port
        server_address = (ip_address, listen_port)
        print('starting up on %s port %s' % server_address)
        sock.bind(server_address)
        # listen for incoming connections
        sock.listen(1)
        conn_list = []
        while True:
            # wait for a connection
            conn, addr = sock.accept()
            conn_list.append(conn)
            print("\nListen thread:~$ \n" + str(addr) + " want to connect to you")
            self.updateDisplay("\nListen thread:~$ " + str(addr) + " want to connect to you",
                               format_msg=self.format_bold)

            # handle the connection
            self.handle_connection(conn, ip_address)

    # handle the connection
    def handle_connection(self, conn, ip_address):
        # create a new thread to open a new terminal
        open_terminal_cmd = identify_platform()
        if not open_terminal_cmd:
            print('Unknown platform')
            return 0

        # wait for user input to confirm the connection
        print("\x1b[1A\x1b[2K", end="")
        # print('Do you want to connect to ' + str(conn.getpeername()) + '? (y/n)')
        self.updateDisplay('\nDo you accept the connection' + '? (y/n)',
                           format_msg=self.format_bold)
        self.listen_thread_input_sign.put(True)
        user_input = self.listen_thread_input_queue.get()
        self.listen_thread_input_sign.queue.clear()
        if user_input == 'y' or user_input == 'Y' or user_input == 'yes' or user_input == 'Yes':
            # send a confirmation message to the client
            random_port = random.randint(1024, 65535)
            message = 'confirm ' + str(random_port)
            conn.send(message.encode())
            # open a new terminal
            self.new_terminal_server(ip_address, random_port)
            print("\x1b[1A\x1b[2K", end="")
            print('Connection established')
            now = datetime.datetime.now()
            date_string = now.strftime("%m, %d, %Y")
            username1 = 'this client'
            ip_addr1 = ip_address
            username2 = 'unknown'
            ip_addr2 = str(conn.getpeername())
            sqlite_op.insert_history_connections(date_string, username1, ip_addr1, username2, ip_addr2,
                                                 'passive, success')
            # print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
        elif user_input == 'n' or user_input == 'N' or user_input == 'no' or user_input == 'No':
            # send a rejection message to the client
            conn.send('reject'.encode())
            conn.close()
            print("\x1b[1A\x1b[2K", end="")
            print('Connection closed')
            now = datetime.datetime.now()
            date_string = now.strftime("%m, %d, %Y")
            username1 = 'this client'
            ip_addr1 = ip_address
            username2 = 'unknown'
            ip_addr2 = str(conn.getpeername())
            sqlite_op.insert_history_connections(date_string, username1, ip_addr1, username2, ip_addr2,
                                                 'passive, failure')
            # print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
        else:
            print("\x1b[1A\x1b[2K", end="")
            print('\nUnknown command, connection closed')
            now = datetime.datetime.now()
            date_string = now.strftime("%m, %d, %Y")
            username1 = 'this client'
            ip_addr1 = ip_address
            username2 = 'unknown'
            ip_addr2 = str(conn.getpeername())
            sqlite_op.insert_history_connections(date_string, username1, ip_addr1, username2, ip_addr2,
                                                 'passive, failure')
            conn.send('reject'.encode())
            conn.close()

    # update display
    def updateDisplay(self, message, format_msg=None):
        cursor = self.chatDisplay.textCursor()
        if format_msg is None:
            cursor.insertText(message)
        else:
            cursor.insertText(message, format_msg)
            # set format to default
            cursor.insertText(" ", self.format_default)

        self.chatDisplay.verticalScrollBar().setValue(self.chatDisplay.verticalScrollBar().maximum())


def identify_platform():
    if sys.platform == 'darwin':
        return 'open -a Terminal'
    # elif sys.platform == 'win32':
    #     return 'start cmd'
    # elif sys.platform == 'linux':
    #     return 'gnome-terminal'
    else:
        return False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = P2P_Chat_Console()
    window.show()
    sys.exit(app.exec_())
