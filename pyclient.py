#!/usr/bin/python3

import socket
import threading

serverAdress = ( "192.168.0.190", 20001 )
buffersize = 1024
info=""
srvmsg=""

UDPClientSoc = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def screen():
	#print("\033c", end="")
	print('\x1b[2J', end="")
	print(info)
	print(srvmsg)


def listen():
	print("listening ")
	global info
	global srvmsg
	while(True):
		msg = UDPClientSoc.recvfrom(buffersize)
		print(msg[0].decode("utf8"))
		info = "connected to {}".format(msg[1])
		srvmsg += msg[0].decode("utf8") + "\n"
		screen()
		if msg == b'q':
			break
	
t1 = threading.Thread(target=listen,args=())
t1.start()
    
	

while(True):
	usrmsg = input("type a msg : ")
	bytesToSend = str.encode(usrmsg)
	UDPClientSoc.sendto(bytesToSend, serverAdress)

	
