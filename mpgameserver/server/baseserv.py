from mpgameserver import GameServer

class TestServer(GameServer):
    def on_message(self, client, message):
        print(f"Received from client: {message}")
        response = f"Echo: {message}"
        self.send(client, response)

if __name__ == "__main__":
    server = TestServer()
    server.start()
