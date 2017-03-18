'''
A text communication server that encrypts messages received and send using the RSA 
algorithm. 
The idea is that, we have a Client object which contains the connection socket as 
well as a set of private and public RSA keys. The private key will be the key that 
the server uses to decrypt messages received from the client. The public key will
be the key that the server uses to encrypt messages to be sent to the client. It 
must be received from the client. The public key generated as the keypair with the 
private key must be sent to the client.
'''
import socket
import time
from collections import deque
from threading import Thread, current_thread

MSGLEN = 512 #each msg should be 512 or less chars 
   
class Server:
    
        
    def __init__(self):
        #create an INET, STREAMing socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket, making it public; anyone can connect to the socket (localhost, ip, PC name...)
        self.s.bind(('',8029))
        #now actually become publicly accessible
        self.s.listen(5)
        self.socks = deque()
        self.begin_loop()
        return
    
    def send(self, sock, msg):
        try:
            writer = sock.makefile(mode='w')
            writer.write(msg)
            writer.flush()
            writer.close()
        except RuntimeError:
            #remove the client that caused the issue and continue
            self.socks.remove(sock)
            print('error sending, removing sock')
        return
    
    def broadcast(self, message):
        #loop through clients, calling send() on each of them
        for sock in self.socks:
            try:
                writer = sock.makefile(mode='w')
                writer.write(message)
                writer.flush()
                writer.close()
            except RuntimeError:
                #remove the client that caused the issue and continue
                self.socks.remove(sock)
                print('error sending, removing sock')
                continue
        return
    
    '''function should be called on a new thread, dedicated to listening for a new message'''
    def handle_client(self, sock):
        while 1:
            #recv() msg from client
            try:
                print("waiting for rcv")
                msg = sock.recv(MSGLEN)
                print("after rcv")
                if msg == b'':
                    current_thread()
                    raise RuntimeError("socket connection broken")
            
                self.broadcast(msg.decode('utf-8'))
                print("msg recv: ", msg)
            except RuntimeError:
                # break out of the thread if the message was not received properly
                #and also remove the client from clients
                self.socks.remove(sock)
                return
        return
    
    def test(self, sock):
        print("New thread. Sleeping and sending hello!")
        time.sleep(5)
        self.send(sock, "Hello world")
        return
     
         
    def begin_loop(self):
        while 1:
            #wait for a connection to occur
            (clientsocket, address) = self.s.accept()

            '''
            Now clientsocket needs to be passed on to a child thread
            and set up for broadcasting, etc... One way to do this 
            (and I will use this method) is creating a new class that
            contains the client's info, including the clientsocket. 
            So when we broadcast, we can just loop through the client 
            instances and write to their sockets. The client class will
            also, eventually, be responsible for containing the client's 
            public RSA key when encryption is implemented.
            '''
            self.socks.append(clientsocket)
            print("Client created")
            #create a new thread with the function called
            Thread(target=self.handle_client,args=(clientsocket,)).start()
            Thread(target=self.test, args=(clientsocket,)).start()
        return


print("Starting server...")
Server()
