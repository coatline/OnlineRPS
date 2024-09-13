from threading import Thread, Lock
from rooms import Rooms
import socket
import json

class UDP_Server(Thread):
    def __init__(self, udp_port, lock : Lock, rooms : Rooms) -> None:
        Thread.__init__(self)
        self.lock = lock
        self.rooms = rooms
        self.is_listening = True
        self.udp_port = int(udp_port)
        
        
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.udp_port))
        self.sock.setblocking(0)
        self.sock.settimeout(5)
        
        while self.is_listening:
            try:
                data, address = self.sock.recvfrom(1024)
            except socket.timeout:
                continue

            try:
                data = json.loads(data)
                try:
                    identifier = data['identifier']
                except KeyError:
                    identifier = None

                try:
                    room_id = data['room_id']
                except KeyError:
                    room_id = None

                try:
                    payload = data['payload']
                except KeyError:
                    payload = None

                try:
                    action = data['action']
                except KeyError:
                    action = None

                if room_id not in self.rooms.rooms.keys():
                    print("Room not found")
                    return
                
                self.lock.acquire()
                
                try:
                    if action == "send_to_all":
                        try:
                            self.rooms.send_to_all(identifier, room_id, payload['message'])
                        except:
                            pass
                    elif action == "send_to":
                        try:
                            self.rooms.send_to(identifier, room_id, payload['recipients'], payload['message'])
                        except:
                            pass
                finally:
                    self.lock.release()

            except KeyError:
                print("Json from %s:%s is not valid" % address)
            except ValueError:
                print("Message from %s:%s is not valid json string" % address)

        self.stop()

    def stop(self):
        self.sock.close()

    