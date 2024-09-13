from threading import Thread, Lock
from rooms import Rooms
from user import User
import socket
import json

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
                user_id = None
                room_id = None
                payload = None

                try:
                    user_id = data['identifier']
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
                    self.route(conn, addr, action, payload, user_id, room_id)
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
        
    def route(self, sock, addr, action, payload, user_id = None, room_id = None):
        if action == "register":
            print(f"Registered user with port: {int(payload)}")
            user = self.rooms.register_new_user(addr, int(payload))
            # send success and user's identifier
            user.send_tcp(True, user.identifier, sock)
            return
        else:
            if user_id not in self.rooms.users.keys():
                print(f"Unknown user identifier: {user_id}")
                sock.send(json.dumps({"success" : "False", "message": "Unknown identifier"}))
                return
            
            user : User = self.rooms.users[user_id]

            if action == "create_room":
                room_identifier = self.rooms.create_room(payload)
                self.rooms.join_user(user.identifier, room_identifier)
                # send the client their current room_id
                user.send_tcp(True, room_identifier, sock)
            elif action == "get_rooms":
                # get the room, room_id, room_name, player_count, capacity
                rooms = []
                for room_id, room, in self.rooms.rooms.items():
                    rooms.append({"room_id": room_id, "room_name": room.name,
                                    "player_count": len(room.users), "room_capacity": room.capacity})
                user.send_tcp(True, rooms, sock)
            elif action == "leave_room":
                try:
                    if room_id not in self.rooms.rooms:
                        raise RoomNotFound()
                    self.rooms.leave(user_id, room_id)
                    user.send_tcp(True, room_id, sock)
                except RoomNotFound:
                    user.send_tcp(False, room_id, sock)
                except NotInRoom:
                    user.send_tcp(False, room_id, sock)
                

    def stop(self):
        self.sock.close()
        
        
class RoomNotFound(BaseException): pass
class NotInRoom(BaseException): pass