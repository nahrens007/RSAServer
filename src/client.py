import socket
import rsa
from threading import Thread

class Client:
    
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        