from threading import Lock
from server_types import UDP_Server, TCP_Server
from rooms import Rooms

def main_loop(tcp_port, udp_port):

    print("-------------------------------------")
    print(f"Starting Server on ports:\ntcp: {tcp_port}\nudp: {udp_port}")    

    rooms = Rooms(2)    
    lock = Lock()
    udp_server = UDP_Server(udp_port, lock, rooms)
    tcp_server = TCP_Server(tcp_port, lock, rooms)
    # start the threads
    udp_server.start()
    tcp_server.start()

    is_running = True

    while is_running:
        command = input("running > ")

        if command == "quit":
            udp_server.is_listening = False
            tcp_server.is_listening = False
            is_running = False
    
    # wait until the threads are finished.
    udp_server.join()
    tcp_server.join()

if __name__ == "__main__":
    main_loop(7777, 7777)
    quit()