import socket
import pickle
from threading import Thread

class TCPClient:
    def __init__(self, ip, port, gui):
        self.gui = gui
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, int(port)))
        listener = Thread(target=self.listen)
        listener.setDaemon(True)
        listener.start()

    def send(self, message):
        message = pickle.dumps(message)
        self.sock.send(message)

    def listen(self):
        while True:
            data = self.sock.recv(2048)
            if not data:
                break
            data = pickle.loads(data)
            if data[0] == 'MESSAGE':
                print(data[1])
            else:
                self.gui.update_gui(data[1])
