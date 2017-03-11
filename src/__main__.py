'''
A text communication server that encrypts messages received and send using the RSA 
algorithm. 
'''
import socket
import rsa
from collections import deque

    
class Server:
    class Client:
        '''
        The server will use a different private key for each client that connects. 
        So the client class is responsible for containing the server's private key 
        for the client instance as well. 
        '''
        def __init__(self, sock):
            self.sock = sock
            #self.pub_key = pub_key #encrypt with this key (clients actual public key)
            #self.priv_key = ser_priv_key #decrypt with this key
            self.listen()
            return
        
        def listen(self):
            #this method will wait for a message to be received from the client
            pass
        
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
        pass
        
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
            self.clients.append(clientsocket)
            self.handle(clientsocket)
        return

if __name__ == '__main__':
    pass
