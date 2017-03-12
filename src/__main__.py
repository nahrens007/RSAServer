'''
A text communication server that encrypts messages received and send using the RSA 
algorithm. 
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
        (self.pub, self.priv) = rsa.newkeys(1024)
        return
    
    def send(self, msg):
        #write msg to self.sock
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        return
    
    def get_sock(self):
        return self.sock
    def get_pub(self):
        return self.pub
    def recv(self, len):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                current_thread()
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks) #need to decode msg first
    
   
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
    
    '''Create a new thread dedicated to listening on the client's socket'''
    def handle_client(self, client):
        sock = client.get_sock()
        client.send(client.get_pub()) # send the servers public key to the client
        while 1:
            #recv() msg from client
            try:
                msg = client.recv(MSGLEN)
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
