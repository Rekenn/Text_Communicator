from threading import Thread
import socket
from queue import Empty

class ClientThread(Thread):
	
	def __init__(self, client_socket, messages):
		Thread.__init__(self)
		self.BUF_SIZE = 1024
		self.client_socket = client_socket
		self.message = None
		self.queue_messages = messages
		self.disconnected = False
		self.handlers = {
						's': self.__handle_send,
						'r': self.__handle_receive,
						'd': self.__handle_disconnect
}

	def run(self):		
		while not self.disconnected:
			self.message = self.client_socket.recv(self.BUF_SIZE)
			self.handlers[self.__decode_message()]()

	def __handle_send(self):
		self.queue_messages.put(self.message[1:])
		self.queue_messages.join()

	def __handle_receive(self):
		try:
			response = self.queue_messages.get(False)
		except Empty:
			return
		self.client_socket.send(response)
		self.queue_messages.task_done()

	def __handle_disconnect(self):
		self.queue_messages.put(self.message[1:] + b'disconnected')
		self.queue_messages.join()
		self.disconnected = True

	def __decode_message(self):
		handler = self.message.decode()
		return handler[0]
