import socket
import pickle
from threading import Thread
from rov import ROV

class TCPServer:

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(5)
        self.rov = ROV()
        self.connections = []
        self.listen_for_connections()

    def listen_for_connections(self):
        while True:
            conn, addr = self.sock.accept()
            connection = Connection(conn, addr, self)
            self.connections.append(connection)

    def send_telemetry(self):
        telemetry = self.rov.update_status()
        telemetry = pickle.dumps(('TELEMTRY', telemetry))
        for connection in self.connections:
            connection.conn.send(telemetry)

    def send_message(self, message):
        message = pickle.dumps(('MESSAGE', message))
        for connection in self.connections:
            connection.conn.send(message)

class Connection:

    def __init__(self, conn, addr, server):
        self.conn = conn
        self.ip = addr[0]
        self.port = addr[1]
        self.server = server
        self.client_type = None
        self.listener = Thread(target=self.listen)
        self.listener.start()

    def listen(self):
        while True:
            command = self.conn.recv(2048)
            if not command or command[0] == 'DISCONNECT_CLIENT':
                self.disconnect()
                break
            command = pickle.loads(command)
            if command[0] == 'CONNECT_CLIENT':
                self.connect(command[1])
            if isinstance(command, tuple):
                function = self.server.rov.commands[command[0]]
                function(command)
            else:
                function = self.server.rov.commands[command]
                function()
            self.server.send_telemetry()

    def connect(self, client_type):
        self.client_type = client_type
        print(self.client_type + ' @ ' + str(self.ip) + ' has connected')
        self.server.send_message(
            '{} connected to ROV @ {}'.format(self.client_type, self.ip)
        )

    def disconnect(self):
        self.conn.close()
        self.server.connections.remove(self)
        print(self.client_type + ' @ ' + str(self.ip) + ' has disconnected')
