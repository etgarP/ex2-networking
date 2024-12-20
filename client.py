import socket
import sys
import os

BUFFER_SIZE = 1024
OK = 200
REDIRECT = 301
NOT_FOUND = 404

def main():
	serverIp = sys.argv[1] 
	serverPort = int(sys.argv[2])
	# Creating socket
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try_again = False
	closed_connection = True

	while True:
		# If it's in redirect we don't want to get input
		if (not try_again):
			filePath = input().replace(" ", "")
		try_again = False
		fileName = get_file_name(filePath)
		# If the connection is closed we restart it
		if (closed_connection):
			s.close()
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((serverIp,serverPort))
			closed_connection = False
		request = construct_msg(filePath, try_again)
		s.send(request.encode())
		# Getting reply from the server
		serverReply = get_all_data(s)
		if (not serverReply):
			closed_connection = True
			try_again = True
			continue
		# Getting the first line
		status, firstLine, fileContent, linesDict = parse_response(serverReply)
		print(firstLine.decode())
		if(status == OK):
			create_the_file(fileContent, fileName)
			if (connection_closed(linesDict)):
				closed_connection = True
			continue
		elif(status == REDIRECT):
			filePath = get_location(linesDict)
			try_again = True
		closed_connection = True


def get_file_name(filePath):
	return "index.html" if filePath == "/" else os.path.basename(filePath)

def get_leftover(newData):
	status, firstLine, fileContent, linesDict = parse_response(newData)
	if "Content-Length" in linesDict:
		length = int(linesDict["Content-Length"])
		fileLength = len(fileContent)
		return length - fileLength
	return 0

def get_all_data(con):
	data = b""
	start = True
	leftover = 5000
	while leftover:
		# Adding up the data
		newData = con.recv(BUFFER_SIZE)
		if start and newData:
			leftover = get_leftover(newData)
			start = False
		else:
			leftover -= len(newData)
		if not newData: 
			break
		data += newData
	if (data == b""):
		return None
	return data

def get_content(data):
	delimiter = b"\r\n\r\n"
	# Finding the separation in the server's message
	index = data.find(delimiter)
	return data[index + len(delimiter):]
    
def create_the_file(fileContent, fileName):
	# Getting the directory that this file is in
	current_directory = os.path.dirname(os.path.abspath(__file__))
	# Creating the path to the new file
	file_path = os.path.join(current_directory, fileName)
	# If the file is an image, write in bytes
	if fileName.endswith(('.ico', '.jpg')):
		with open(file_path, "wb") as file:
			file.write(fileContent)
		file.close()
	else:
		fileContent = fileContent.decode()	
		# Writing the content to the file
		with open(file_path, "w") as file:
			file.write(fileContent)
		file.close()
	


def get_first_line(serverReply):
	response = serverReply
	lines = response.splitlines()
	return lines[0]


def get_location(lines):
    return lines.get("Location", "")

def construct_msg(path, redirectFlag):
	if (not redirectFlag):
		return 	(f"GET {path} HTTP/1.1\r\n"
				f"Connection: keep-alive\r\n"
				f"\r\n")
	return 	(f"GET {path} HTTP/1.1\r\n"
			f"Connection: close\r\n"
			f"\r\n")


def parse_response(serverReply):
	firstLine = get_first_line(serverReply)
	statusCode = int(firstLine.decode().split(" ")[1])
	if (statusCode == OK):
		file = get_content(serverReply)
	else:
		file = None	
	# separating the reply into lines
	delimiter = b"\r\n\r\n"
	index = serverReply.find(delimiter)
	headers_section = serverReply[:index].decode()
	lines = headers_section.splitlines()
	headers = lines[1:]
	headers_dict = {}
	for header in headers:
		if header:
			key, value = header.split(":", 1)
			headers_dict[key.strip()] = value.strip()

	return statusCode, firstLine, file, headers_dict

def connection_closed(linesDict):
	return linesDict.get("connection", "").lower() == "close"


if __name__ == "__main__":
    main()
