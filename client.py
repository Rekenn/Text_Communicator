import socket
from threading import Thread
from sys import exit

MENU_MESSAGE = """Default settings
Username: User
Host: 0.0.0.0
Port: 2222
If you want to change settings press -c"""

class Client:

	def __init__(self, name="User", host="0.0.0.0", port=2222):
		self.host = host
		self.port = port
		self.name = name.encode()
		self.BUF_SIZE = 1024
		self.client_socket = None
		self.connected = False
		self.recv_thread = Thread(target=self.__recv_msg)
		self.protocol = {
						"SEND": b's' + self.name + b': ',
						"RECEIVE": b'r',
						"DISCONNECT": b'd' + self.name + b' '
}
		self.__connect()
	
	def __connect(self):
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.client_socket.connect((self.host, self.port))
		except socket.error:
			print("Can't connect to the server")
			exit()
		print("You are connected properly!")
		self.connected = True

	def __send_msg(self):
		while self.connected:
			message = input()
			if message == "exit":
				self.__send_protocol("DISCONNECT")
				break
			self.__send_protocol("SEND", message)
		self.connected = False

	def __recv_msg(self):
		while self.connected:
			self.__send_protocol("RECEIVE")
			self.client_socket.settimeout(0.1)
			try:
				message = self.client_socket.recv(self.BUF_SIZE)
			except ConnectionResetError:
				self.connected = False
			except socket.timeout:
				continue
			else:
				print(message.decode())

	def __send_protocol(self, protocol, message=''):
		try:
			self.client_socket.send(self.protocol[protocol] + message.encode())
		except BrokenPipeError:
			print("Problem with server")
			self.connected = False

	def start_conversation(self):
		self.recv_thread.start()
		self.__send_msg()
		self.__close_statements()

	def __close_statements(self):
		self.recv_thread.join()
		self.client_socket.close()

def client_menu():
	print(MENU_MESSAGE)
	client = None
	settings = input()
	if settings == "-c":
		name = input("Enter username: ")
		host = input("Enter host: ")
		port = int(input("Enter port: "))
		client = Client(name=name, host=host, port=port)
	else:
		print("Started with default settings.")
		client = Client()
	client.start_conversation()

if __name__ == "__main__":
	client_menu()
