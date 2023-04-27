import queue
import socket
import sys
import threading
from time import sleep

quit_queue = queue.Queue()


def receive_message(conn, addr):
    try:
        while True:
            # Receive message from the other side
            data = conn.recv(1024)

            if not data:
                # If the other side closes the connection, break the loop
                break
            if data.decode() == 'q':
                quit_queue.put('q')
                break

            # Print the message received from the other side
            print(f"Message from {addr[0]}:{addr[1]}: {data.decode()}")

        # Close the socket connection
        conn.close()
    except Exception as e:
        print('connection closed')
        return e


def server(ip, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind IP address and port number
    s.bind((ip, port))

    # Listen on the port and wait for connections
    s.listen(1)
    print(f"Listening on port {port}...")

    while True:
        # Wait for a client connection
        conn, addr = s.accept()
        print(f"Connected to client {addr[0]}:{addr[1]}")

        # Start a new thread to handle client communication
        t = threading.Thread(target=receive_message, args=(conn, addr))
        t.start()

        # Send message to the client
        while True:
            message = input("Enter message (enter q to quit): ")

            if not quit_queue.empty():
                break

            if message == "q":
                # If user enters q, break the loop
                s.sendall(message.encode())
                sleep(1)
                break

            # Send message to the client
            conn.sendall(message.encode())

        # Close the socket connection
        conn.close()
        return 0


def client(ip, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    s.connect((ip, port))

    # Start a new thread to handle server communication
    t = threading.Thread(target=receive_message, args=(s, (ip, port)))
    t.start()

    # Send message to the server
    while True:
        message = input("Enter message (enter q to quit): ")

        if not quit_queue.empty():
            break

        if message == "q":
            # If user enters q, break the loop
            s.sendall(message.encode())
            sleep(1)
            break

        # Send message to the server
        s.sendall(message.encode())

    # Close the socket connection
    s.close()
    return 0


def server_unittest():
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server listening on {}:{}'.format(*server_address))

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        client_socket, client_address = server_socket.accept()
        print('Accepted connection from {}'.format(*client_address))

        # Receive the data in small chunks and retransmit it
        data = client_socket.recv(1024)
        print('Received data:', data.decode())
        client_socket.sendall(data)

        # Clean up the connection
        client_socket.close()
        print('Connection closed')
        break


def client_unittest():
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's address and port
    server_address = ('localhost', 8080)
    client_socket.connect(server_address)

    # Send some data
    message = 'Hello from the client'.encode()
    client_socket.sendall(message)

    # Receive the response
    data = client_socket.recv(1024)
    print('Received response:', data.decode())

    # Clean up the connection
    client_socket.close()
    print('Connection closed')


if __name__ == "__main__":
    # Get command line arguments
    if len(sys.argv) != 4:
        print("Usage: python communication.py <server/client> <ip> <port>")
        sys.exit()

    mode = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])

    if mode == "server":
        server(ip, port)
    elif mode == "client":
        sleep(2)
        client(ip, port)
    else:
        print("Invalid mode, please use 'server' or 'client'")
        sys.exit()
