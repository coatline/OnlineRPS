

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

    def is_empty(self) -> bool:
        return len(self.users) == 0

    def is_full(self) -> bool:
        return len(self.users) == self.capacity


class RoomFull(BaseException): pass