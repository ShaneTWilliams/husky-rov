import socket
import pickle
from PyQt5.QtCore import QThread, pyqtSignal
from threading import Thread

class TCPClient:

    def __init__(self, ip, port, gui):
        self.gui = gui
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, int(port)))
        self.listener = ListenerThread(self.sock, self.gui)
        self.listener.start()
        self.send(('CONNECT_CLIENT', 'COPILOT'))

    def send(self, message):
        message = pickle.dumps(message)
        self.sock.send(message)

class ListenerThread(QThread):

    data_signal = pyqtSignal(tuple)

    def __init__(self, sock, gui):
        QThread.__init__(self)
        self.sock = sock
        self.gui = gui

    def run(self):
        while True:
            data = self.sock.recv(2048)
            if not data:
                self.data_signal.emit(('MESSAGE', 'gone'))
                break
            data = pickle.loads(data)
            self.data_signal.emit(data)
