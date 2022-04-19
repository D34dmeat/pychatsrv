#!/usr/bin/python3

import threading
import socket

localIP = "192.168.0.190"
localPort = 20001
buffersize = 1024
run = True
clients = []
clientinfo={}
info=""
srvmsg=""

greeting = "hello this is served"
bytesToSend = str.encode(greeting)


# create datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# bind to address and port

UDPServerSocket.bind((localIP, localPort))

print("udp server is running")

def send( msg, client):
    bytemsg = str.encode(msg)
    UDPServerSocket.sendto(bytemsg, client)

def sendAll( msg):
    bytemsg = str.encode(msg)
    for client in clientinfo:
        #print("{}".format(clientinfo[client]))
        UDPServerSocket.sendto(bytemsg, clientinfo[client]["fulladress"])
    
def screen():
    #print("\033c", end="")
    print('\x1b[2J', end="")
    print(info)
    print(srvmsg)
        
        

# listen for datagrams
def listen():
    global run
    global srvmsg
    global info
    while(run):
        byteAdressPair = UDPServerSocket.recvfrom(buffersize)
        message = byteAdressPair[0]
        adress = byteAdressPair[1]
        if clients.count(adress) == 0:
            clients.append(adress)
            clientinfo["{}".format(adress)] = {"alias" : "anon", "adress" : clients.index(adress), "fulladress":adress}
            
            mess = "{} just connected".format( clientinfo["{}".format(adress)]["alias"])
            sendAll(mess)
                
                
                
        
        #print("clients {} ".format( clients))
        
        
        if message.decode("utf8").startswith("#alias"):
            oldalias = clientinfo["{}".format(adress)]["alias"]
            clientinfo["{}".format(adress)]["alias"] = message.decode("utf8").replace("#alias", "").strip()
            sendAll("{} just changed name to {}".format(oldalias,clientinfo["{}".format(adress)]["alias"]))
        if run == False:
            print("shutting down")
            break
     
        clientMsg = "{} > {}\n".format(clientinfo["{}".format(adress)]["alias"],message.decode("utf8"))
        srvmsg += clientMsg
        info = "connection to clients: "
        for client in clientinfo:
            info += "{} {}, ".format(clientinfo[client]["alias"],clientinfo[client]["fulladress"])
        #print(clientMsg)
        screen()
        if message == b'q':
            print("message q")
            run = False
            
        if message == b'#greet':
            with open('./srvtxt/greeting', encoding='utf8') as f:
                for line in f:
                    bytemsg = str.encode(line)
                    UDPServerSocket.sendto(bytemsg, adress)
                
                
                
        if not message.decode("utf8").startswith("#"): 
                
            response = "{} > {}\n".format(clientinfo["{}".format(adress)]["alias"],message.decode("utf8"))
        #bytemsg = str.encode(response)
        
        #for client in clientinfo:
                #mess = "{} just connected".format( clientinfo[client]["alias"])
                #print(mess)
        
            # sending reply
            sendAll(response)
        
        # sending reply
        #UDPServerSocket.sendto(bytemsg, adress)

t1 = threading.Thread(target=listen,args=())
t1.start()

while(run):
    
    screen()
    lask = input("#&")
    print(lask)
    if lask ==  "quit":
        run = False
        print("exit")
        break
        
    if lask.startswith("send"):
        print(clients)
        messg = lask.replace("send","server admin > ")
        srvmsg += messg +"\n"
        for client in clients:
            send(messg, client)
            
            


