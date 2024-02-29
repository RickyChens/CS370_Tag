import socket
import threading
import pickle

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            position = pickle.loads(data)
            print("Received position:", position)

            # Send a response to the client
            response = pickle.dumps("Position received")
            client_socket.sendall(response)
        except:
            break

    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)
    server_socket.listen()

    print("Server is listening on", server_address)

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connected to:", client_address)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
