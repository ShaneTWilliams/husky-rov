import time
import pickle

from app.tcp_client import TCPClient


class PneumaticsComputer:
    def __init__(self, port):
        self.client = TCPClient()
        self.port = port
        self.connect_loop()

    def connect_loop(self):
        while True:
            error = self.client.connect(self.port, '192.168.2.99')
            if error:
                time.sleep(1)
                continue
            try:
                print('Connected!')
                self.send(('CONNECT_CLIENT', 'PNEUMATICS'))
                self.control_loop()
            finally:
                self.client.disconnect()

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
            except:
                continue
            if data['claw']['claw_closed']:
                pass
            else:
                pass
