import socket
import sys
from os import listdir, getcwd
from os.path import isfile, join

SERVER_MODE = 0
USER_MODE = 1

SERVER_IP_IDX = 2
SERVER_PORT_IDX = 3
LISTENING_PORT_IDX = 4

IP_IDX = 1
PORT_IDX = 2
FILE_NAME_IDX = 0

def send_file(filename, conn):
	# open file on the client side
	f = open(filename,'rb')
	l = f.read(1024)
	while (l):
		conn.send(l)
		l = f.read(1024)
	f.close()

def download_file(file_name, s):
	with open(file_name, 'wb') as f:
		while True:
			data = s.recv(1024)
			if not data:
				break
			# write data to a file
			f.write(data)
	f.close()

def server_mode():
	if len(sys.argv) != 5:
		raise Exception("wrong number of arguements for Server Mode!")

	# connect to the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((sys.argv[SERVER_IP_IDX], int(sys.argv[SERVER_PORT_IDX])))

	# scan files on current working directory
	cwd = getcwd()
	files_in_dir = [f for f in listdir(cwd) if isfile(join(cwd,f))]

	# send information about listening port and files shared
	msg = "1" + " " + sys.argv[LISTENING_PORT_IDX] + " " + ','.join(files_in_dir)
	s.send(msg.encode())
	s.close()

	# wait for connection from anybody
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('0.0.0.0', int(sys.argv[LISTENING_PORT_IDX])))
	server.listen(5)

	while True:
		client_socket, client_address = server.accept()
		requested_file = client_socket.recv(1024).decode()
		# send the file to the client
		send_file(requested_file, client_socket)
		client_socket.close()

def user_mode():
	while True:
		# connect to the server
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((sys.argv[SERVER_IP_IDX], int(sys.argv[SERVER_PORT_IDX])))

		# send file name to search
		file_to_seek = input("Search: ")
		msg = "2 " + file_to_seek
		s.send(msg.encode())

		# print results
		search_results = s.recv(1024).decode().split(",")
		if search_results[0] != "\n":
			for i in range(len(search_results)):
				print(str(i+1) + " " + search_results[i].split(" ")[FILE_NAME_IDX])

			# choose from menu the desired file
			selection = int(input("Choose: ")) -1
			file_info = search_results[selection].split(" ")

			# connect to user that has the file
			server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server.connect((file_info[IP_IDX], int(file_info[PORT_IDX])))
			server.send(file_info[FILE_NAME_IDX].encode())

			# get the file
			download_file(file_info[FILE_NAME_IDX], server)
			server.close()
		
	s.close()

def illegal():
	raise Exception("Invalid Task Selected")

def main():
	if len(sys.argv) < 4:
		raise Exception("missing arguements!")
	mode = int(sys.argv[1])
	switcher = {
		SERVER_MODE: server_mode,
		USER_MODE: user_mode
	}
	return switcher.get(mode, illegal)()

if __name__ == "__main__":
	# args:
	# [0] = program name
	# [1] = mode
	# [2] = server ip
	# [3] = server port
	# [4] = listening port (optional for Server Mode)
	main()