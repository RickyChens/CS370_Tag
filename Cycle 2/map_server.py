import socket
import threading
import pickle
from randomMap import generate_random_map

random_map = generate_random_map()

class Server:
    def __init__(self, host='localhost', port=5555):
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
            if message == b'get_start':
                client.sendall(b'start')
            elif message == b'get_clients':
                print(f'Sending clients to: {client}')
                client.sendall(pickle.dumps(len(self.clients)))
                print(f'Clients: {self.clients} Finished Sending')
            elif message == b'get_map':
                print("test")
                print("Serialize Map Start")
                serialized_map = pickle.dumps(random_map)
                print("Serialize Map Finished")
                print("Start Sending Map")
                client.send(serialized_map)
                print("Finished Sending Map")
            else:
                print(f'Received message: {message} from client: {client}')


    def run(self):
        while True:
            client, addr = self.server.accept()
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


server = Server()
server.run()
