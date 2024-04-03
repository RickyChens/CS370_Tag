from mpgameserver import UdpClient, Timer
import time
import sys

def main():  # pragma: no cover

    addr = ('127.0.0.1', 5555)
    client = UdpClient()

    dt = 0
    interval = 1/30

    def send_message():
        if client.connected():
            client.conn.send(b"hello")

    def onConnect(connected):
        if not connected:
            print("unable to connect to server")
            sys.exit(1)

    timer = Timer(.5, send_message)

    client.connect(addr, callback=onConnect)

    try:
        while True:
            timer.update(interval)
            client.update()
            while msg := client.getMessage():
                print(msg, "Latency: %dms" % int(1000*client.latency()))
            time.sleep(interval)
    except KeyboardInterrupt as e:
        pass

    client.disconnect()
    client.waitForDisconnect()

if __name__ == '__main__':
    main()