import os 
import sys 
import socket

def get_all_data(con):
    """
        input: 
            con: connection
        output:
            all the data in a variable
    """
    data = ""
    data = con.recv(BUFFER_SIZE)
    return data.decode()

def parse_request(data):
    """
        input: 
	        data
        output:
            path, lines in a map in format (name: value), if its a .ico or .jpg
    """
    # separating the data into lines
    lines = data.splitlines()

    # First line is the GET request. the path is in the middle
    request_line = lines[0]
    _, path, _ = request_line.split(" ")
    headers = lines[1:]

    headers_dict = {}
    for header in headers:
        if header:
            key, value = header.split(":", 1)
            headers_dict[key.strip()] = value.strip()
    _, extension = os.path.splitext(path)
    is_ico_jpg = extension.lower() in ['.ico', '.jpg']
    return path, headers_dict, is_ico_jpg

def path_exists(relative_path):
    """
        input: 
            relative path
        output:
            if relative path is null or doesn't exist returns false 
                else return true
    """
    if not relative_path:
        return False, None

    # Normalize relative path
    base_path = os.path.join(os.path.dirname(__file__), "files")
    relative_path = os.path.join(base_path, relative_path.lstrip('/'))

    # Check if path exists
    if os.path.exists(relative_path):
        return True, relative_path
    return False, None

def get_message(full_path, is_ico_jpg, closed):
    """
        input: 
            path, is_ico_jpg, closed
        output:
            needed message to send to client
    """
    try:
        # Open in binary mode for `.jpg` or `.ico`, text mode otherwise
        if closed:
            connection_status = "closed"
        else:
            connection_status = "keep alive"
        mode = "rb" if is_ico_jpg else "r"
        with open(full_path, mode) as f:
            content = f.read()
            message = f"HTTP/1.1 200 OK\r\n"
            message += f"Connection: {connection_status}\r\n"
            message += f"Content-Length: {len(content)}\r\n"
            message += "\r\n"
            if (mode == "r"):
                content = content.encode()
            return message.encode() + content
    except Exception as e:
        return get_not_exist_message()

def get_redirect_message():
    """
        input: 
            nothing
        output:
            the not exist message
    """
    message = "HTTP/1.1 301 Moved Permanently\r\n"
    message += "Connection: close\r\n"
    message += "Location: /result.html\r\n"
    message += "\r\n"
    return message.encode()

def get_not_exist_message():
    """
        input: 
            nothing
        output:
            the not exist message
    """
    message = "HTTP/1.1 404 Not Found\r\n"
    message += "Connection: close\r\n"
    message += "\r\n"
    return message.encode()

def is_closed(lines):
    """
        input: 
            lines
        output:
            if the connection is closed
    """
    return lines.get("connection", "").lower() == "close"

TCP_IP = '0.0.0.0'
try:
    TCP_PORT = int(sys.argv[1])
    if TCP_PORT < 1024 or TCP_PORT > 65535:
        raise ValueError("Port must be between 1024 and 65535")
except ValueError as e:
    print(f"Invalid port: {e}")
    sys.exit(1)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
BUFFER_SIZE = 1024
s.listen(1)

while True:
    conn, addr = s.accept()
    conn.settimeout(1.0)
    try:
        while True:
            data = get_all_data(conn)	
            print(data)
            if not data or len(data.strip()) == 0:
                conn.close()
                break
            path, lines, is_ico_jpg = parse_request(data)
            closed = is_closed(lines)
            if path == "/":
                path = "/index.html"
            if path == '/redirect':
                message = get_redirect_message()
            else:
                exists, full_path = path_exists(path)
                if not exists:
                    message = get_not_exist_message()
                else:
                    message = get_message(full_path, is_ico_jpg, closed)
            conn.send(message) 
    except Exception as e:
        conn.close()


