import socket
import pickle
from threading import Thread

class Client:
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
            rov_status = self.sock.recv(2048)
            if not rov_status:
                break
            rov_status = pickle.loads(rov_status)
            self.gui.update_gui(rov_status)
