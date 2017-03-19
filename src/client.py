import socket
import rsa
from threading import Thread

class Client:
    
    def __init__(self, ip, port):
        (self.pub, self.priv) = rsa.newkeys(1024) #generate 1024 bit key pair
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip,port))
        # send pub key to server; keep priv key.
        # receive the server's public key
        try:
            pub = self.sock.recv(512)
            self.server_pub = rsa.key.PublicKey.load_pkcs1(pub, 'PEM')
        except OSError:
            return
        except:
            print("Server shut down...")
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            raise RuntimeError('Server shut down')
            return
        if pub == b'':
            print("server shut down")
            return
        
        

    def send(self, msg):
        msg = rsa.encrypt(msg.encode(), self.server_pub)
        sent = self.sock.sendall((str(msg) + '\r\n').encode())
        if sent is not None:
            raise RuntimeError("socket connection broken")
        return

    def stop(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        return
    
    def receive(self):
        while True:
            try:
                msg = self.sock.recv(512)
            except OSError:
                break
            except:
                print("Server shut down...")
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                break
            if msg == b'':
                raise RuntimeError("socket connection broken")
            
            print(msg)
        return
    
#ip = input('ip address: ')
#port = int(input('port: '))
ip = 'localhost'
port = 8029
client = Client(ip, port)
rcvThread = Thread(target=client.receive)
rcvThread.start()
while True:
    msg = input()
    if msg == 'exit':
        client.stop()
        break
    client.send(msg)
