import socket
import time

MSGLEN = 512 #each msg should be 512 or less chars 
   
class Server:
    
        
    def __init__(self):
        #create an INET, STREAMing socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #bind the socket, making it public; anyone can connect to the socket (localhost, ip, PC name...)
        self.s.bind(('',8029))
        #now actually become publicly accessible
        self.s.listen(5)
        self.begin_loop()
        return
         
    def begin_loop(self):
        while 1:
            #wait for a connection to occur
            (clientsocket, address) = self.s.accept()

            clientsocket.sendall(b'Hello, world!\r\n')
            print("sleep(2)")
            time.sleep(2)
            print('shutting down socket')
            clientsocket.shutdown(socket.SHUT_RDWR)
            clientsocket.close()
        return


print("Starting server...")
Server()
