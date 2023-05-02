# This is the API doc for P2P Pro

## Central Server Service - central_server.py

For the central server service, it is a Flask app, so it can be run directly.

This is the core of the P2P Pro project. It is a central server service written in Python. It is used to manage the connection between clients and provide the IP address of the client to other clients.

APIs (If not specified, the method is GET): 
1. /register: register a new user so that it can be used to log in to the P2P Pro program.
2. /login: login with a username and password, if the username and password are correct, it will return a token, which can be used to access other APIs.
3. /online: get a list of online users.
4. /add_client: add a new client to the online list.
5. /delete_client: delete a client from the online list.
6. /upload (POST): upload a file to the server, it will return a file id, which can be used to download the file.
7. /download: download a file from the server, it will return the file content, copy the link to the browser, and you can download the file.
8. /storage: get a list of files stored in the server.

## P2P Chat Console with GUI - console_GUI.py

This is a P2P chat program written in Python. It is based on the console version, but it has a GUI interface and more functions.

Just as its base version, it allows multiple clients to connect to a user and communicate with each other.

In this program, there is only one console window for all functions, you can call functions by using buttons, so it's easy to use.

Compared to the console version, this version has a GUI interface, so it's more user-friendly. In addition, it has more functions, such as sending files, sending images.

In addition, chatting with other clients is using different processes, so it won't block the main process, you can continue to using other functions while chatting with other clients, including connecting to other clients and receive new connections.

If you want to run it with command line, you can use the following command:
```shell
python console_GUI.py <username>
```

## Communication Program with GUI - comm_GUI.py

This is a communication program written in Python. This is a Python program for socket communication. It can be used to establish a connection between two machines and send/receive messages.

In this version, comm_GUI also has a GUI interface, calling it separately is not easy because it needs more arguments. So it is recommended to use it with console_GUI.py.

### Using server mode
Directly using the file:
```shell
python communication.py server <ip> <port> <path> <username> <path>
```

ip is the ip address of the server be bind to

port is the port of the server listens to

### Using client mode
Directly using the file:
```shell
python communication.py client <ip> <port> <path> <username> <path>
```