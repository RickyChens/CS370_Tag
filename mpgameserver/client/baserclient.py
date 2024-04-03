from mpgameserver import GameClient

class TestClient(GameClient):
    def on_message(self, message):
        print(f"Received from server: {message}")

    def run(self):
        while True:
            message = input("Enter message to send: ")
            self.send(message)

if __name__ == "__main__":
    client = TestClient("localhost", 8000)
    client.connect()
    client.run()
