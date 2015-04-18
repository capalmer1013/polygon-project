__author__ = 'Brent'

import socket
class mysocket:
    MSGLEN = 1024
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < self.MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)

#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket()         # Create a socket object
port = 1337                # Reserve a port for your service.
#s.bind(("", port))        # Bind to the port


s.connect(("10.8.62.228", 1337))

if s is None:
    print("Couldn't open socket connection")

#c, addr = s.accept()     # Establish connection with client.
#print 'Got connection from', addr

s.sendall("Thank you for connecting\n")

y = s.recv(10)
print(y)

s.close()                # Close the connection
