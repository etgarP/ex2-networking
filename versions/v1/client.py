import socket,sys
from time import sleep

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BUFFER_SIZE = 1024
MESSAGE = b'Foo, World!'
MESSAGE1 = b'bar, Hello'

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((TCP_IP, TCP_PORT))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)

sleep(5)

s1.send(MESSAGE1)
data = s1.recv(BUFFER_SIZE)
s1.close()

data = s.recv(BUFFER_SIZE)
s.close()