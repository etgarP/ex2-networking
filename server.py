import os 
import sys 
import socket
# def fun():
#     """
#         input: 
#             N
#         output:
#             N
#     """
TCP_IP = '0.0.0.0'
TCP_PORT = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
BUFFER_SIZE = 1024
def getAllData(con):
    """
        input: 
            con: connection
        output:
            all the data in a variable
    """
    data = ""
    while True:
        newData = con.recv(BUFFER_SIZE)
        if not newData: 
            break
        newData = str(newData.decode())
        data += newData

while True:
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)	
    parsed = parseRequest()