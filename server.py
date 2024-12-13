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
s.listen(1)

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
        newData = newData.decode()
        data += newData
    return data

def parseRequest():
    """
        input: 
            data
        output:
            path, lines in a map in format (name: value)
    """
def pathExists(relative_path):
    """
        input: 
            relative path
        output:
            if relative path is null or doesnt exists returns false 
                else return true
    """
    if (relative_path and relative_path[0] == '\\'):
        relative_path = "files" + relative_path
    elif (relative_path):
        relative_path = "files\\" + relative_path
    else:
        return False, None
    if os.path.exists(relative_path):
        return True, relative_path
    return False, None

def getMessage(path, lines):
    """
        input: 
            path, lines
        output:
            needed message to send to client
    """

def getClosedMessage():
    """
        input: 
            nothing
        output:
            the closed message needed return
    """

def getNotExistMessage():
    """
        input: 
            nothing
        output:
            the not exist message
    """

def isClosed(lines):
    """
        input: 
            lines
        output:
            if the connection is closed
    """

while True:
    conn, addr = s.accept()
    conn.settimeout(1.0)
    try:
        while True:
            data = getAllData(conn)	
            path, lines = parseRequest()
            exists, path = pathExists(path)
            if not exists:
                message = getNotExistMessage()
                conn.send(message) 
            message = getMessage(path, lines)
            conn.send(message) 
            if isClosed(lines):
                conn.close()
                break
    except Exception as e:
        message = getClosedMessage()
        conn.send(message) 
        conn.close()


