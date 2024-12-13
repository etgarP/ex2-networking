import socket,sys

TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(0)

while True:
	conn, addr = s.accept()
	print('New connection from:', addr)

	conn1, addr1 = s.accept()
	print('New connection from:', addr1)

	data = conn1.recv(BUFFER_SIZE)	
	print("received:", data)
	conn.send(data[0:7]) 

	data = conn.recv(BUFFER_SIZE)	
	print("received:", data)
	conn1.send(data[0:5]) 

	conn.close()
	conn.close()