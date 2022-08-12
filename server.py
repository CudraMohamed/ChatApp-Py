#implementing server side
from email import message
from ipaddress import ip_address
import socket
import select
import sys

from _thread import *

#AF_NET= address domain of the socket
#used for internet domain with two hosts
#type of socket=SOCK_STREAM -  means data are read in continous flow

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#check for sufficient arguments
if len(sys.argv) !=3:
    print("Correct usage: script, IP address, port number")
    exit()

#takes 1st argument from command prompt as IP address
IP_address=str(sys.argv[1])

#takes second arg from command prompt as port
Port=int(sys.argv[2])

#binding server to an ip address and specified port number
server.bind(IP_address, Port)

#listens for 100 dif connections, num can be increased as per convinience
server.listen(100)
list_of_clients=[]
def clientthread(conn, addr):

    #sends message to client whose object is conn
    conn.send("Welcome to this chatroom!")

    while True:
        try:
            message=conn.recv(2048)
            if message:

                #prints message and address of user sent on the server terminal
                print("<" + addr[0] +">" +message)

                #Calls broadcast function to send message to all
                message_to_send="<" + addr[0] +">" + message
                broadcast(message_to_send,conn)

            else:

                #if connection broken,message may lack content,we remove connection

                remove(conn)

        except:
            continue

#broadcasting message to all clients 
def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()

                #if link broken,remove client
                remove(clients)

#removes object from list created in the beginning of the program
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:

    #accept connection request and store 2 parameters ,conn= socket obj for user and addr=Ip addree of client that just connected
    conn, addr=server.accept()

    #maintain list of clients for ease of broadcasting to all available in the room
    print(addr[0] + "connected")

    #cretes an individual thread for every user that connects
    start_new_thread(clientthread,(conn,addr))

conn.close()
server.close()
