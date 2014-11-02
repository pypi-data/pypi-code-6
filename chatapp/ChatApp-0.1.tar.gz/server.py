#!/usr/bin/python3

import socket
import threading

clients=[]
    
def run(clientSocket):
    while True:
        message = clientSocket.recv(2048)
        if not message:
            break
        for allClients, allArress in clients:
            allClients.send(b''+message)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((socket.gethostname(),4096))
serverSocket.listen(5)

for x in range(5):
    print('waiting for client')
    (clientSocket,address)=serverSocket.accept()
    print('connected to '+address[0])
    print('pushing into clients lists')
    clients.append((clientSocket,address))
    print('starting a thread for '+address[0]+'\n')
    theThread=threading.Thread(target=run, args=(clientSocket,))
    theThread.start()