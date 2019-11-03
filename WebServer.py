# Usage: Open terminal/cmd and run "python WebServer.py"

# Import socket module
from socket import * 
# Import Thread
from threading import Thread
# In order to terminate the program
import sys


# Handles incomming connections
def accept_incoming_connections(serverSocket):
    while True:
        # Set up a new connection from the client
        connectionSocket, addr = serverSocket.accept()
        print("%s:%s has connected." % addr)
        # Start client thread to handle the new connection
        Thread(target=handle_client, args=(connectionSocket,)).start()
        
# Handles a single client connection, taking connection socket as argument
def handle_client(connectionSocket):
        # If an exception occurs during the execution of try clause
	# the rest of the clause is skipped
	# If the exception type matches the word after except
	# the except clause is executed
	try:
		# Receives the request message from the client
		message = connectionSocket.recv(1024).decode()

		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filename = message.split()[1]
		#print(filename)
		# Because the extracted path of the HTTP request includes 
		# a character '\', we read the path from the second character 
		f = open(filename[1:], 'rb')
		# Store the entire content of the requested file in a temporary buffer
		data = f.read()
		# Send the HTTP response header line to the connection socket
		connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
		connectionSocket.send(data)
		connectionSocket.send("\r\n".encode()) 
		
		# Close the client connection socket
		connectionSocket.close()

	except IOError:
		# Send HTTP response message for file not found
		connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
		connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
		# Close the client connection socket
		connectionSocket.close()

def main():
        # Create a TCP server socket
        #(AF_INET is used for IPv4 protocols)
        #(SOCK_STREAM is used for TCP)
        serverSocket = socket(AF_INET, SOCK_STREAM)

        # Assign a port number
        serverPort = 1234

        # Bind the socket to server address and server port
        serverSocket.bind(('', serverPort))

        # Listen to at most 5 connections at a time
        serverSocket.listen(5)

        # Server should be up and running and listening to the incoming connections
        print('The server is ready to receive')

        # Start the accepting connections thread
        acceptThread = Thread(target=accept_incoming_connections, args=(serverSocket,))
        acceptThread.start()
        # Wait for the accepting connections thread to stop
        acceptThread.join()
        
        # Close the server socket
        serverSocket.close()  
        # Terminate the program after sending the corresponding data
        sys.exit()

if __name__ == "__main__":
    main()
