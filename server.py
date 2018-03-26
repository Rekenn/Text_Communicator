import socket
from client_thread import ClientThread
from queue import Queue
import time

SERVER_MESSAGE = """Default settings
Host: 0.0.0.0
Port: 2222
If u want to change settings press -c"""

class Server:
	
	def __init__(self, host="0.0.0.0", port=2222):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind((host, port))
		self.server_socket.listen(5)
		self.queue_messages = Queue()
		self.connected_clients = 0
		self.MAX_CLIENTS = 2
		self.clients = []

	def echo_clients(self):
		while self.connected_clients < self.MAX_CLIENTS:
			print("Waiting for client ", self.connected_clients + 1)
			client_socket, addr = self.server_socket.accept()
			print("Client connected from", addr[0], "id", addr[1])
			thread = ClientThread(client_socket, self.queue_messages)
			thread.start()
			self.clients.append(thread)
			self.connected_clients += 1
		self.__server_loop()

	def __server_loop(self):
		while self.connected_clients > 0:
			for client in self.clients:
				if not client.is_alive():
					self.connected_clients -= 1
			time.sleep(1)
		self.__close_threads()
		self.__close_socket()

	def __close_threads(self):
		for client in self.clients:
			client.disconnected = True
			client.join()

	def __close_socket(self):
		self.server_socket.shutdown(socket.SHUT_RDWR)
		self.server_socket.close()

def server_menu():
	print(SERVER_MESSAGE)
	settings = input()
	server = None
	if settings == "-c":
		host = input("Enter hostname: ")
		port = int(input("Enter port: "))
		server = Server(host, port)
	else:
		print("Started with default settings.")
		server = Server()
	server.echo_clients()

if __name__ == '__main__':
	server_menu()
