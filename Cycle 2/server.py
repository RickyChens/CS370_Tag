import socket
import threading
import pickle
from randomMap import generate_random_map

random_map = generate_random_map()
serialized_map = pickle.dumps(random_map)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

class Server:
    def __init__(self, host=ip_address, port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.game_state = {}

    def broadcast(self, message, sender_client):
        for client in self.clients:
            if client != sender_client:
                client.send(message)

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(1024)
                serialized_data = pickle.loads(data)
                if serialized_data == "game finished":
                    # print("finished")
                    finished = pickle.dumps("finished")
                    self.broadcast(finished, client)
                elif serialized_data == "coord":
                    print("hi")
                elif serialized_data == "map":
                    # print("sending map")
                    client.send(serialized_map)
                    # ("finished sending map")
                elif data and data != "coord":
                    player_data = pickle.loads(data)
                    self.broadcast(data, client)
                    # print(player_data)

            except Exception as e:
                print(f"Error: {e}")
                self.clients.remove(client)
                client.close()
                break

    def run(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


server = Server()
server.run()
