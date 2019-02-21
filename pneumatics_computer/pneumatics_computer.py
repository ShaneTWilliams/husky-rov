import pickle
import time
from app.tcp_client import TCPClient


def main():
    port = input('Enter a port to connect to: ')
    PneumaticsComputer(port)


class PneumaticsComputer:
    def __init__(self, port):
        self.client = TCPClient()
        self.port = port
        self.connect_loop()

    def connect_loop(self):
        while True:
            error = self.client.connect(self.port, '192.168.2.99')
            if error:
                print(error)
                time.sleep(1)
                continue
            try:
                self.control_loop()
            except KeyboardInterrupt:
                self.client.send(('DISCONNECT_CLIENT', 'PNEUMATICS'))
                raise KeyboardInterrupt

    def control_loop(self):
        while True:
            try:
                data = self.client.sock.recv(2048)
            except:
                continue
            if not data:
                self.client.disconnect()
                break
            try:
                data = pickle.loads(data)
            except pickle.UnpicklingError:
                continue
            if data['claw']['claw_closed']:
                pass
            else:
                pass


if __name__ == '__main__':
    main()
