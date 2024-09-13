class Room:
    def __init__(self, identifier, capacity, room_name) -> None:
        self.capacity = capacity
        self.users = []
        self.identifier = identifier

        if room_name is not None:
            self.name = room_name
        else:
            self.name = self.identifier

    def join_user(self, user):
        if not self.is_full():
            self.users.append(user)
        else:
            raise RoomFull()

    def leave_user(self, user):
        self.users.remove(user)

    def send_udp_to(self, receiving_user_id, message):
        for user in self.users:
            if user.identifier == receiving_user_id:
                user.send_udp(receiving_user_id, message)

    def send_udp_to_all(self, sender_id, message):
        # print(f"sending {message} from {sender_id} to all")
        for user in self.users:
            if user.identifier != sender_id:
                user.send_udp(sender_id, message)

    def is_user_in_room(self, user_id):
        for user in self.users:
            if user.identifier == user_id:
                return True
        return False

    def is_empty(self) -> bool:
        return len(self.users) == 0

    def is_full(self) -> bool:
        return len(self.users) == self.capacity


class RoomFull(BaseException): pass