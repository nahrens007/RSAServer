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
import rsa
from collections import deque
from threading import Thread, current_thread

MSGLEN = 512 #each msg should be 512 or less chars 

class Client:
    '''
    The server will use a different private key for each client that connects. 
    So the client class is responsible for containing the server's private key 
    for the client instance as well. 
    '''
    def __init__(self, sock):
        self.sock = sock
        ''' 
        self.pub is now what we send the client for when the client sends to the server.
        self.priv is what the server uses to decrypt data received from the client.
        Since generating a new keypair takes several seconds, it may be a better idea to wait
        until a new thread is created to generate the keys
         '''
        (self.pub, self.priv) = rsa.newkeys(1024) #generate 1024 bit key pair
        #create a file writer out of the socket instead of writing directly
        #to the socket
        self.writer = self.sock.makefile(mode='w')
        self.send(str(self.pub))# send the server's public key to the client
        return
    
    def send(self, msg):
        #write msg to self.sock
        '''Unlike send(bytes), the sendall(bytes) method continues to send data from bytes until either all 
        data has been sent or an error occurs. None is returned on success. On error, an 
        exception is raised, and there is no way to determine how much data, if any, was 
        successfully sent.'''
        '''sent = self.sock.sendall(str(msg).encode('utf-8'))
        if sent is None:
            print("sent msg successfully!")
        else:
            print("did not send msg!")'''
        # write using file writer instead of raw socket
        self.writer.write(msg)
        self.writer.flush()
        return
    
    def get_sock(self):
        return self.sock
    def get_pub(self):
        return self.pub
    def recv(self):
        msg = self.sock.recv(MSGLEN)
        if msg == b'':
            current_thread()
            raise RuntimeError("socket connection broken")
        return msg.decode('utf-8') #need to decode msg before returning
    
   
class Server:
    
        
    def __init__(self):
        #create an INET, STREAMing socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket, making it public
        self.s.bind((socket.gethostname(),8029))
        #now actually become publicly accessible
        self.s.listen(5)
        self.clients = deque()
        self.begin_loop()
        return
    
    def broadcast(self, message):
        #loop through clients, calling send() on each of them
        for client in self.clients:
            try:
                client.send(message)
            except RuntimeError:
                #remove the client that caused the issue and continue
                self.clients.remove(client)
                continue
        return
    
    '''function should be called on a new thread, dedicated to listening for a new message'''
    def handle_client(self, client):
        while 1:
            #recv() msg from client
            try:
                msg = client.recv()
                print("msg recv: ", msg)
            except RuntimeError:
                # break out of the thread if the message was not received properly
                #and also remove the client from clients
                self.clients.remove(client)
                return
            self.broadcast(msg)
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
            new_client = Client(clientsocket)
            self.clients.append(new_client)
            #create a new thread with the function called
            Thread(target=self.handle_client,args=(new_client,)).start()
        return

if __name__ == '__main__':
    print("Starting server...")
    Server()
