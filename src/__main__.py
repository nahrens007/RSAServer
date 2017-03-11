'''
A text communication server that encrypts messages received and send using the RSA 
algorithm. 
'''
import socket

class Server:
    def __init__(self):
        #create an INET, STREAMing socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket, making it public
        self.s.bind((socket.gethostname(),8029))
        #now actually become publicly accessible
        self.s.listen(5)
        self.begin_loop()
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
            
        return

if __name__ == '__main__':
    pass
