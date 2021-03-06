import socket
import pickle


class TCPClient:

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

    def disconnect(self):
        self.send(('DISCONNECT_CLIENT', 'PNEUMATICS'))
        self.sock.shutdown(socket.SHUT_WR)

    def send(self, message):
        message = pickle.dumps(message)
        self.sock.send(message)
