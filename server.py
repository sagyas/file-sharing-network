import socket, threading
import sys

IP_IDX = 0
PORT_IDX = 1
FILES_IDX = 2

REGISTER = 1
SEARCH = 2
CASE_IDX = 0

class Client:
	def __init__(self, _address_):
		self.address = _address_
		self.files = []

	def add_file(self,file):
		self.files.append(file)

	def get_files_contains_substr(self, substr):
		lst = []
		for file in self.files:
			if substr in file.get_name():
				lst.append(file)
		return lst

	def get_address(self):
		return self.address

class File:
	def __init__(self, file_name, address):
		self.file_name = file_name
		self.address = address

	def get_name(self):
		return self.file_name
	
	def get_address(self):
		return self.address

	def get_port(self):
		return self.address[PORT_IDX]

	def get_ip(self):
		return self.address[IP_IDX]

	def __lt__(self,other):
		return self.get_name() < other.get_name()

class FilesMenu:
	def __init__(self, _files_):
		self.files = _files_

	def add_file(self, file):
		self.files.append(file)

	def get_files(self):
		return self.files

	def get_as_msg(self):
		if len(self.files) == 0:
			return "\n"

		self.files.sort()
		msg = ""
		i = 1
		for file in self.files:
			msg += file.get_name() + " " + file.get_ip() + " " + file.get_port() + ","
			i+=1
		msg = msg[:-1]
		msg += '\n'
		return msg

	def get_file(self, index):
		return self.files[index]

# check the format of the cmd sender to the server
def is_cmd_valid(msg):
	result = 0
	if msg[CASE_IDX] == "1" and len(msg)>=3:
		result = 1
	elif msg[CASE_IDX] == "2" and len(msg)==2:
		result = 1
	return result

def is_valid_selection(selection, menu):
	try:
		converted_selection = int(selection)
	except:
		return 0

	if converted_selection > len(menu.get_files()):
		return 0
	
	return converted_selection

def error_msg(sender_info, socket):
	line = "Illegal request"
	socket.sendto(line, sender_info)

def illegal():
	raise Exception("Invalid Task Selected")

def register_routine(client_address, client_socket, data, clients):
	# create new client with his shared files
	address = (client_address[IP_IDX],data[PORT_IDX])
	client = Client(address)
	shared_files = data[FILES_IDX].split(",")
	for file in shared_files:
		client.add_file(File(file, address))
	
	# add client to list
	clients.append(client)

def search_routine(client_address, client_socket, data, clients):
	file_to_search = data[1]
	matching_files = []

	# add all files which contains file_to_search
	for client in clients:
		matching_files.extend(client.get_files_contains_substr(file_to_search))

	# create menu of files and send in to client
	menu = FilesMenu(matching_files)
	client_socket.send(menu.get_as_msg().encode())

	
def main():
	# listen to anybody
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('0.0.0.0', int(sys.argv[PORT_IDX])))
	server.listen(5)

	clients = []

	while True:
		# accept connection and get data
		client_socket, client_address = server.accept()
		data = client_socket.recv(1024).decode()
		data = data.split(" ")

		if is_cmd_valid(data):
			case = int(data[CASE_IDX])
			switcher = {
				REGISTER: register_routine,
				SEARCH: search_routine
			}
			switcher.get(case, illegal)(client_address, client_socket, data, clients)
		
		client_socket.close()

if __name__ == "__main__":
	main()