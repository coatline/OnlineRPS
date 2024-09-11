from threading import Thread, Lock
from rooms import Rooms
import socket
import json
import time

class UDP_Server(Thread):
    def __init__(self, port, lock : Lock, rooms : Rooms) -> None:
        Thread.__init__(self)
        
        self.port = port
        self.lock = lock
        self.rooms = rooms
        self.is_listening = True

    
class TCP_Server(Thread):
    def __init__(self, port, lock : Lock, rooms : Rooms) -> None:
        Thread.__init__(self)
        
        self.port = port
        self.lock = lock
        self.rooms = rooms
        self.is_listening = True
    
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # listen on all available network interfaces using 0.0.0.0
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.setblocking(0)
        self.sock.settimeout(5)
        self.sock.listen(1)

        while self.is_listening:
            # wait until we can establish a connection
            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue

            print(f"Accepted connection to {addr}.")

            data = conn.recv(1024)

            try:
                data = json.loads(data)
                action = data['action']
                identifier = None
                room_id = None
                payload = None

                try:
                    identifier = data['identifier']
                except KeyError:
                    pass
                
                try:
                    room_id = data['room_id']
                except KeyError:
                    pass 

                try:
                    payload = data['payload']
                except KeyError:
                    pass 

                self.lock.acquire()

                try:
                    self.route(conn, addr, action, payload, identifier, room_id)
                finally:
                    self.lock.release()

            except KeyError:
                print("Json from %s:%s is not valid" % addr)
                conn.send("Json is not valid")
            except ValueError:
                print("Message from %s:%s is not valid json string" % addr)
                conn.send("Message is not a valid json string")
            
            conn.close()
            
        self.stop()
        
    def route(self, sock, addr, action, payload, identifier = None, room_id = None):
        if action == "register":
            print("registered")
            user = self.rooms.register_new_user(addr, int(payload))
            # send success and user's identifier
            user.send_tcp(True, user.identifier, sock)
            return

    def stop(self):
        self.sock.close()