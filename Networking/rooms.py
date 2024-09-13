from room import Room, RoomFull
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

    def remove_empty_rooms(self):
        for room_id in list(self.rooms.keys()):
            if self.rooms[room_id].is_empty():
                del self.rooms[room_id]

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
    
    def send_to(self, identifier, room_id, message):
        room = self.rooms[room_id]
        room.send_udp_to(identifier, message)
    
    def send_to_all(self, user_id, room_id, message):
        print("here")
        if room_id not in self.rooms:
            print("room id not found")
            raise RoomNotFound()
         
        room : Room = self.rooms[room_id]
         
        if not room.is_user_in_room(user_id):
            print("user id not found in room")
            raise NotInRoom()
        
        print("sending")
        room.send_udp_to_all(user_id, message)
    
    def try_join_user_to(self, user_id, room_name) -> any:
        try:
            user = self.users[user_id]
            
            for room in self.rooms.values():
                if room.name == room_name:
                    room.join_user(user)
                    return room.identifier
        except RoomFull():
            return None
            
    def auto_join_user(self, user_id):
        user = self.users[user_id]

        for room_id in self.rooms.keys():
            room = self.rooms[room_id]
            if not room.is_full():
                room.join_user(user)
                return room_id

        # there are no available rooms
        # create a new one
        room_id = self.create_room()
        self.rooms[room_id].join_user(user)
        return room_id
        
    def leave_user(self, user_id, room_id):
        user = self.users[user_id]
        self.rooms[room_id].leave_user(user)

class NotInRoom(BaseException): pass
class RoomNotFound(BaseException): pass