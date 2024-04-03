
import sys
import pygame
from mpgameserver import UdpClient, EllipticCurvePublicKey
from mpgameserver import *

bg_color = (0,0,200)

def onConnect(connected):
    global bg_color

    if connected:
        # on connection success change the background to green
        bg_color = (0,200,0)
    else:
        # on connection timeout change the background to red
        bg_color = (200,0,0)

def main():
    """
    Usage:
        python template_client.py [--dev]

        --dev: optional, use development keys
    """
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 60
    host = 'localhost'
    port = 1474

    screen = pygame.display.set_mode((640, 480))

    client = UdpClient()
    client.connect((host, port), callback=onConnect)

    while True:

        dt = clock.tick(FPS) / 1000

        # TODO: process events, update game world, render frame, send messages

        screen.fill(bg_color)

        client.update()

        for msg in client.getMessages():
            try:
                # TODO: process message
                print(msg)
            except Exception as e:
                logging.exception("error processing message from server")

        pygame.display.flip()

    pygame.quit()

    if client.connected():
        client.disconnect()
        client.waitForDisconnect()

if __name__ == '__main__':
    main()
