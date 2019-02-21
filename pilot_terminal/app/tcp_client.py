import socket
import pickle
from PyQt5.QtCore import QThread, pyqtSignal


class TCPClient:

    def __init__(self):
        self.listener = ListenerThread(self)
        self.is_connected = False

    def connect(self, port, ip):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((ip, int(port)))
        except ValueError:
            return 'Invalid port'
        except ConnectionRefusedError:
            return 'Connection refused by ROV'
        except OverflowError:
            return 'Port number out of range'
        except socket.timeout:
            return 'Connection attempt timed out'
        except socket.gaierror:
            return 'Invalid IP'
        except ConnectionResetError:
            return 'Connection reset by ROV'
        except OSError:
            return 'Host unreachable - verify network connection'
        self.listener.start()
        self.is_connected = True

    def disconnect(self):
        self.sock.shutdown(socket.SHUT_WR)
        self.listener.quit()
        self.is_connected = False

    def send(self, message):
        message = pickle.dumps(message)
        self.sock.send(message)


class ListenerThread(QThread):

    data_signal = pyqtSignal(dict)

    def __init__(self, client):
        QThread.__init__(self)
        self.client = client

    def run(self):
        while True:
            data = self.client.sock.recv(2048)
            if not data:
                self.client.sock.close()
                break
            data = pickle.loads(data)
            self.data_signal.emit(data)
