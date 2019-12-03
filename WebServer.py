from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json

# Set up chat server
# Store client sockets
clients = {}

HOST = ''
PORT = 1234


BUFSIZ = 1024
ADDR = (HOST, PORT)

# Create a TCP server socket
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
file = open("JsonHolder.txt", "w")


# Handles incomming connections
def accept_incoming_connections():
    while True:
        # Set up a new connection from the chat client
        client, client_address = SERVER.accept()
        # print("%s:%s has connected." % client_address)
        # Send greeting message
        client.send("Welcome to the IOT server, please enter a name before transmission begins".encode("utf8"))
        # Start client thread to handle the new connection
        Thread(target=handle_client, args=(client,)).start()


# Handles a single client connection, taking client socket as argument
def handle_client(client):
    # Get name from chat client
    name = client.recv(BUFSIZ).decode("utf8")
    # Send welcome message to chat client
    welcome = 'You may begin transmission, if you ever want to quit, type {quit} to exit.'
    client.send(welcome.encode("utf8"))
    # Add new pair client socket, name to the clients pool
    clients[client] = name

    while True:
        # Receive message from client
        msg = client.recv(BUFSIZ).decode("utf8")
        # If it is not a {quit} message from client, then broadcast the
        # message to the rest of the connected chat clients
        # Else server acks the {quit} message, deletes the client from
        # the chat pool, and informs everyone
        if msg != "{quit}":
            msg_print = json.loads(msg)
            msg_string = json.dumps(msg_print).encode("utf8")
            print(msg_print)
            if clients[client] != "Graph":
                broadcast(msg_string)
                file.write(msg)
        else:
            print(clients[client], "has left.")
            client.send("{quit}".encode("utf8"))
            client.close()
            del clients[client]
            file.close
            break


# Broadcasts a message to all the clients, using prefix for name identification
def broadcast(msg_string):
    for sock in clients:
        sock.send(msg_string)


def main():
    # Start listening to client connections
    SERVER.listen(5)
    print("Waiting for connection...")
    # Start the accepting connections thread
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    # Wait for the accepting connections thread to stop
    ACCEPT_THREAD.join()


    # Close the server socket
    SERVER.close()


if __name__ == "__main__":
    main()
