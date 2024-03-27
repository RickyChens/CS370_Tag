import socket
import threading
import pickle
from randomMap import generate_random_map
class Server:
    def __init__(self, host = 'localhost', port = 5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        self.game_state = {}

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client):
        ready_count = 0
        client_ready_status = {client: False for client in self.clients}
        while True:
            message = client.recv(1024)
            if message == b'ready':
                client_ready_status[client] = True
                if all(client_ready_status.values()):
                    for client in self.clients:
                        client.sendall(b'start')
            elif message == b'unready':
                client_ready_status[client] = False
            elif message == b'get_clients':
                client.sendall(pickle.dumps(len(self.clients)))
            elif message == b'get_map':
                random_map = generate_random_map()
                serialized_map = pickle.dumps(random_map)
                client.send(serialized_map)
            else:
                print(f'Received message: {message} from client: {client}')

            if message == b'get_start':
                if ready_count == len(self.clients):
                    client.sendall(pickle.dumps('start'))
    def run(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)

            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

server = Server()
server.run()