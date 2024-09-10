import socket
import pickle
import select

# NOT USED
class Network:

    def __init__(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setblocking(False)
        self.server = "192.168.1.116"
        self.port = 7777
        self.addr = (self.server, self.port)

        print(f"Connecting to host: {self.server} on port: {self.port}")
        self.player = self.connect()

    def connect(self):
        try:
            self.client_socket.connect(self.addr)
            return pickle.loads(self.client_socket.recv(2048))
        except socket.error as e:
            print(f"Error connecting to host. {str(e)}")
    
    def send(self, data):
        try:
            self.client_socket.send(pickle.dumps(data))
            # return pickle.loads(self.client_socket.recv(2048))
        except socket.error as e:
            print(str(e))
    
    def try_receieve_data(self):
        data = self.client_socket.recv(2048)

        if data != None:
            pickled = pickle.loads(data)
            return pickled

    # def check_for_incoming(self):
    #     # List of sockets to check for readability
    #     sockets_to_read = [self.client_socket]
        
    #     # Use select to wait for any of the sockets to become readable
    #     readable, _, _ = select.select(sockets_to_read, [], [])
        
    #     # Iterate over readable sockets
    #     for sock in readable:
    #         if sock == self.client_socket:
    #             # Receive data from the server
    #             try:
    #                 data = pickle.loads(self.client_socket.recv(2048))

    #                 if data:
    #                     print(f"Received: {data.decode()}")
    #                     return data
    #                 else:
    #                     # No more data from the server, connection closed
    #                     print("Connection closed by server")
    #             except socket.error as e:
    #                 # Handle socket error
    #                 print(f"Socket error: {e}")