import math
import socket
import asyncio
import data
import pickle
import threading
import time

def str_to_pos(str):
        str = str.split(',')
        return (int(str[0]), int(str[1]))

def pos_to_str(pos : tuple):
        return str(pos[0]) + "," + str(pos[1])


def send_data(my_socket : socket.socket, data : data.Data):
        try:
                my_socket.send(pickle.dumps(data))
        except WindowsError as e:
                return

async def receive_data(my_socket : socket.socket, timeout = math.inf) -> data.Data:
        loop = asyncio.get_event_loop()

        try:
                data = await asyncio.wait_for(loop.sock_recv(my_socket, 2048), timeout=timeout)
                loaded_data = pickle.loads(data)
                print(f"Received data of type: {loaded_data.header}")
                return loaded_data
        except asyncio.TimeoutError:
                print(f"Receiving data timed out after {timeout} seconds.")
                return None
        except (asyncio.CancelledError, ConnectionResetError):
                print("Connection lost")
                return None
        except Exception as e:
                print(f"An error occurred: {e}")
                return None


def is_connection_alive(my_socket : socket.socket) -> bool:
        # loop = asyncio.get_event_loop()

        try:
                # data = await loop.sock_recv(my_socket, 2048)
                data = my_socket.recv(2048)
                # await loop.sock_sendall(my_socket, "ping".encode())
                if not data:
                        return False
                return True
        except (ConnectionResetError, BrokenPipeError):
                print("Connection lost")
                return False
        except socket.error as e:
                return False


# def setup_connection(server_ip: str, port: int, sock : socket.socket) -> socket.socket:
#     sock.setblocking(False)
#     addr = (server_ip, port)

#     while True:
#         try:
#             print(f"Waiting for connection to server {server_ip} on port {port}")
#             sock.connect(addr)
#             print(f"Connected to {server_ip} on port {port}")
#             return sock  # Return the connected socket if successful
#         except Exception as e:
#             print(f"Unexpected error when trying to connect: {e}")
#             time.sleep(1)



async def setup_connection(server_ip: str, port: int, sock : socket.socket, retry_interval: int = 0.5) -> socket.socket:
        loop = asyncio.get_event_loop()
        sock.setblocking(False)
        addr = (server_ip, port)
        print(f"Waiting for connection to server {server_ip} on port {port}")

        while True:
                try:
                        await asyncio.wait_for(loop.sock_connect(sock, addr), timeout=5)
                        # client_socket.connect(addr)
                        print(f"Connected to {server_ip} on port {port}")
                        return sock  # Return the connected socket if successful
                except(asyncio.TimeoutError, ConnectionRefusedError) as e:
                #     print(f"Connection failed: {e}")
                #     print(f"Retrying in {retry_interval} seconds...")
                        await asyncio.sleep(retry_interval)  # Wait before retrying
                except Exception as e:
                        print(f"Unexpected error: {e}")
                        await asyncio.sleep(retry_interval)