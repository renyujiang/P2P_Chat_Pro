# P2P Pro - EC530
This is EC530 P2P Pro project.

Presentation Link: https://docs.google.com/presentation/d/1jCKI4AsXwgbstk6mi6an6p3H3BnKyAKw_XqlJ0u-bXA/edit?usp=sharing

## Requirements

### <span style="color:red">This program's full function works on macOS only, don't run it on Windows or Linux.</span>

### <span style="color:red">This program's full function works on macOS only, don't run it on Windows or Linux.</span>

### <span style="color:red">This program's full function works on macOS only, don't run it on Windows or Linux.</span>

## P2P Chat Console - console.py

This is a P2P chat program written in Python. It allows multiple clients to connect to a server and communicate with each other.

In this program, there is only one console for all functions, you can call functions by using commands, so it's easy to use.

For example, user can use command "list" to list all connected clients, use command "connect <ip> <port>" to connect to a client with the ip and port, use command "quit" to quit the program.

In addition, chatting with other clients is using different processes, so it won't block the main process, you can continue to using other commands while chatting with other clients, includig connecting to other clients and receive new connections.

### Features of this program:

1. It has connection confirmation process, so you can reject connections from other clients.
2. It has a chat history, so you can see the chat history with other clients.
3. It uses multithreading and multiprocessing, chatting with other clients is continuously, you can send as many messages as you want.
4. Moreover, the processing of connecting other clients is total automatic, you don't need to do anything, just wait for new terminals to show up.
5. Robust, chatting terminal can be closed without affecting the main process and the listening thread wouldn't block the console's main functions.

### How to use

The following commands are available in the chat program:

1. list: List all connected clients
2. connect <ip> <port>: Connect to a client with the ip and port
3. help: Show help text
4. quit: Quit the program

## Communication Program - comm.py

This is a communication program written in Python. This is a simple Python program for socket communication. It can be used to establish a connection between two machines and send/receive messages.

## How to use
This program has two parts, server and client. You can run the server on one machine and run the client on another machine. The server will listen to the port you specified and wait for connections. The client will connect to the server and send/receive messages.

It can either be used as a module or directly using the file.

### Using server mode
Directly using the file:
```shell
python communication.py server <ip> <port>
```

ip is the ip address of the server be bind to

port is the port of the server listens to

### Using client mode
Directly using the file:
```shell
python communication.py client <ip> <port>
```

ip is the ip address of the server

port is the port of the client tries to connect






License
This program is released under the MIT License. See the LICENSE file for details.