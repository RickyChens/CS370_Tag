import socket
import threading
import pickle
from randomMap import generate_random_map

class Server:
    def __init__(self, host='localhost', port=5555):
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
                if data:
                    player_data = pickle.loads(data)
                    # Assuming player_data is a tuple of (x, y)
                    self.broadcast(data, client)
                    print(data)
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
