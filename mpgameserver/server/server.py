
import os
import sys
import logging

from mpgameserver import *

from mpgameserver import EventHandler, ServerContext, TwistedServer, \
    GuiServer, EllipticCurvePrivateKey

class MyGameEventHandler(EventHandler):

    def starting(self):
        pass

    def shutdown(self):
        pass

    def connect(self, client):
        pass

    def disconnect(self, client):
        pass

    def update(self, delta_t):
        pass

    def handle_message(self, client, msg):
        pass

def main():
    """
    Usage:
        python template_server.py [--gui]

        --gui : optional, display the metrics UI
    """

    # bind to an IPv4 address that can be accessed externally.
    host = "localhost"
    port = 5555
    key = None

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(levelname)s %(filename)s:%(funcName)s():%(lineno)d:%(message)s')

    ctxt = ServerContext(MyGameEventHandler())

    # command line switch controls running in headless mode (default)
    # or with the built-in gui server
    if '--gui' in sys.argv:
        server = GuiServer(ctxt, (host, port))
    else:
        server = TwistedServer(ctxt, (host, port))

    server.run()

if __name__ == '__main__':
    main()

