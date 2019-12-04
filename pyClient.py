import socket
import json
import threading
from datetime import datetime

def receive(clientSocket):
    while True:
        message = clientSocket.recv(1024).decode("utf8")
        if not message:
            print('Server closed')
            return
        jParse(message)

def jParse(msg):
    data = json.loads(msg)
    temp.append(data["tempF"])
    humid.append(data["humidity"])
    bright.append(data["brightness"])
    time.append(convertTime(data["time"]))

def convertTime(unixTime):
    return datetime.fromtimestamp(unixTime).strftime("%H:%M:%S")

def getData():
    return time,temp,bright,humid

#create connection
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverName = '' #socket.gethostbyname(socket.gethostname())
serverPort = 1234
clientSocket.connect((serverName,serverPort))

#create new thread for incoming data
threading.Thread(target=receive,args=[clientSocket],daemon=True).start()

#initialize variables for the graph
temp,bright,humid,time = []