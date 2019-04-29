import time
import pickle
import pigpio

from app.tcp_client import TCPClient


class PneumaticsComputer:
    def __init__(self, port):
        self.client = TCPClient()
        self.port = port
        self.pi = pigpio.pi()
        self.connect_loop()

    def connect_loop(self):
        while True:
            error = self.client.connect(self.port, '192.168.2.99')
            if error:
                time.sleep(1)
                print('ici')
                continue
            try:
                print('Connected!')
                self.client.send(('CONNECT_CLIENT', 'PNEUMATICS'))
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
                self.pi.write(22, True)
                print('closed')
            else:
                self.pi.write(22, False)
                print('open')
            if data['air_open']:
                self.pi.write(3, True)
                print('air open')
            else:
                self.pi.write(3, False)
                print('air closed')
