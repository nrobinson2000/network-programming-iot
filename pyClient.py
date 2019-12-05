import socket
import json
import threading
from datetime import datetime
import time as ti

BUFSIZ = 2048

def receive():
    while True:
        message = clientSocket.recv(BUFSIZ).decode("utf8")
        if not message:
            print('Server closed')
            return
        #clientSocket.send('{"testBeep": "beepbop"}'.encode("utf8"))
        # print(message)
        jParse(message)
        

def jParse(msg):
    if (len(msg)==0):
        return
    lines = msg.split(';')
    for line in lines:
        if (len(line)==0):
            continue
        print(line)
        try:
            data = json.loads(line)
        except json.decoder.JSONDecodeError:
            continue
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
serverName = 'localhost'
serverPort = 1234
clientSocket.connect((serverName,serverPort))
clientSocket.send('Graph'.encode())
print('connected')

#initialize variables for the graph
temp,bright,humid,time = [-1],[-100],[-1],[-1]

#create new thread for incoming data
threading.Thread(target=receive).start()
    