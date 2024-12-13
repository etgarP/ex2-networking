import socket
import sys
import os

BUFFER_SIZE = 1024

def main():
	server_ip = sys.argv[1] 
	server_port = int(sys.argv[2])
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((server_ip,server_port))

	while True:
		filePath = input()
		fileName = get_file_name(filePath)
		# Construct msg
		request = (
			f"GET {filePath} HTTP/1.1\r\n"
			f"Connection: keep-alive\r\n"
			f"\r\n"
		)
		# Convert to bytes
		s.send(request.encode('utf-8'))
		# Getting data from the server
		serverReply = get_all_data(s)
		fileContent = get_content(serverReply)

		# Create file and fill it
		create_the_file(fileContent,fileName)


def get_file_name(filePath):
	return os.path.basename(filePath)

def get_all_data(con):
    """
        input: 
            con: socket
        output:
            all the data in a variable
    """
    data = b""
    while True:
        newData = con.recv(BUFFER_SIZE)
        if not newData: 
            break
        data += newData
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
	else:	
	    # Writing the content to the file
	    with open(file_path, "w") as file:
	        file.write(fileContent.decode('utf-8'))


if __name__ == "__main__":
    main()