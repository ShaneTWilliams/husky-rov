import socket
from threading import Thread
import pickle
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
            self.send(
                'MESSAGE',
                '{} connected to ROV @ port {}'.format(connection.client_type, connection.port)
            )

    def send(self, message_type, message):
        message = pickle.dumps((message_type, message))
        for connection in self.connections:
            connection.conn.send(message)

class Connection:

    def __init__(self, conn, addr, server):
        self.conn = conn
        self.addr = addr
        self.ip = addr[0]
        self.port = addr[1]
        self.server = server
        self.client_type = None
        self.listener = Thread(target=self.listen)
        self.listener.start()

    def listen(self):
        while True:
            command = self.conn.recv(2048)
            if not command:
                self.conn.close()
                self.server.connections.remove(self)
                print(self.client_type + ' @ ' + str(self.addr) + ' has disconnected')
                break
            command = pickle.loads(command)
            if command[0] == 'CONNECT_CLIENT':
                self.client_type = command[1]
                print(self.client_type + ' @ ' + str(self.addr) + ' has connected')
            if isinstance(command, tuple):
                function = self.server.rov.commands[command[0]]
                function(command)
            else:
                function = self.server.rov.commands[command]
                function()

            self.server.send('TELEMETRY', self.server.rov.update_status())
