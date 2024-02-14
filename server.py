import socket
import threading
import json

# Server settings
SERVER_IP = '192.168.229.187'  # Listen on all network interfaces
SERVER_PORT = 5555
BUFFER_SIZE = 1024

# Create a socket and bind it to the server IP and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()

print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

# List to keep track of all connected clients
clients = []


def handle_client(client_socket, address):
    print(f"Connection from {address} has been established.")
    clients.append(client_socket)

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(BUFFER_SIZE).decode()
            if not data:
                break  # Connection is closed from client side

            # Here, you would process and possibly broadcast the data
            print(f"Received data from {address}: {data}")


          # Example: broadcasting received data back to all connected clients
       #     for client in clients:
         #       if client != client_socket:  # Optionally prevent sending data back to the sender
          #          client.sendall(data.encode())
    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection from {address} closed.")


while True:
    # Accept new connections
    client_socket, addr = server_socket.accept()
    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()
