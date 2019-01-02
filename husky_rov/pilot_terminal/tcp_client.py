import socket
import pickle
from PyQt5.QtCore import QThread, pyqtSignal


class TCPClient:

    def __init__(self):
        self.listener = ListenerThread(self)
        self.is_connected = False

    def connect(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('192.168.2.99', int(port)))
        self.listener.start()
        self.send(('CONNECT_CLIENT', 'PILOT'))
        self.is_connected = True

    def disconnect(self):
        self.send(('DISCONNECT_CLIENT', 'PILOT'))
        self.sock.shutdown(socket.SHUT_WR)
        self.is_connected = False

    def send(self, message):
        message = pickle.dumps(message)
        self.sock.send(message)


class ListenerThread(QThread):

    data_signal = pyqtSignal(tuple)

    def __init__(self, client):
        QThread.__init__(self)
        self.client = client

    def run(self):
        self.sock = self.client.sock
        while True:
            data = self.sock.recv(2048)
            if not data:
                self.client.sock.close()
                break
            data = pickle.loads(data)
            self.data_signal.emit(data)
