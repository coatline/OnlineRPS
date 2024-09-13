from room import Room
from user import User
import uuid


class Rooms:
    def __init__(self, room_capacity = 2) -> None:
        
        self.rooms = {}
        self.users = {}
        self.room_capacity = room_capacity
    
    # returns the id of the room just created
    def create_room(self, room_name = "") -> str:
            identifier = str(uuid.uuid4())
            self.rooms[identifier] = Room(identifier, self.room_capacity, room_name)
            return identifier

    def register_new_user(self, user_addr, user_udp_port) -> User:
         
        user = None

        for registered_user in self.users.values():
            if registered_user.addr == user_addr:
                user = registered_user
                user.udp_addr = (user_addr[0], user_udp_port)
                break

        if user is None:
            user = User(user_addr, user_udp_port)
            self.users[user.identifier] = user
        
        return user
    
    def send_to_all(self, user_id, room_id, message):
        if room_id not in self.rooms:
            raise RoomNotFound()
         
        room = self.rooms[room_id]
         
        if not room.is_user_in_room(user_id):
            raise NotInRoom()
         
        for user in room.users:
            if user.identifier != user_id:
                user.send_udp(message)
    
    def join_user(self, user_id, room_id):
        self.rooms[room_id].join_user(self.users[user_id])
        
    def leave_user(self, user_id, room_id):
        user = self.users[user_id]
        self.rooms[room_id].leave_user(user)

class NotInRoom(BaseException): pass
class RoomNotFound(BaseException): pass