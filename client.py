#implementing client side of the room
import socket
import select
import sys

from server import IP_address

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) !=3:
    print("Correct usage: script, IP address, port number")
    exit()

IP_address=str(sys.argv[1])
Port=int(sys.argv[2])
server.connect((IP_address, Port))

while True:
    #maintaina list of possible input streams
    sockets_list=[sys.stdin, server]

    #possible inputs include,manual input to send to other people
    #or server is sending a message to be prnted on the screen
    #if server wants to send a message, the if condition=true
    #if user wants to send a message else=true

    read_sockets,write_socket,error_socket=select.select(sockets)

    for socks in read_sockets:
        if socks==server:
            message=socks.recv(2048)
            print(message)

        else:
            message=sys.stdin.readline()
            server.send(message)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()

server.close()