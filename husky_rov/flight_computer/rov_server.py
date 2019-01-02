import socket
import pickle
from threading import Thread
from rov import ROV


class ROVServer:

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.rov = ROV()
        self.connections = []
        self.listen_for_connections()

    def listen_for_connections(self):
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            Connection(conn, addr, self)

    def send_telemetry(self):
        telemetry = self.rov.update_status()
        telemetry = pickle.dumps(('TELEMETRY', telemetry))
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
        self.server.connections.append(self)
        self.client_type = None
        self.listener = Thread(target=self.listen)
        self.listener.start()
        print('Client @ ' + addr[0] + ' has connected')
        self.server.send_message(
            'Client connected to ROV @ {}'.format(self.ip)
        )

    def listen(self):
        while True:
            command = self.conn.recv(2048)
            if not command:
                self.disconnect()
                break
            command = pickle.loads(command)
            if isinstance(command, tuple):
                function = self.server.rov.commands[command[0]]
                function(command)
            else:
                function = self.server.rov.commands[command]
                function()
            self.server.send_telemetry()

    def disconnect(self):
        print('Client @ ' + str(self.ip) + ' has disconnected')
        self.server.send_message(
            'Client disconnected from ROV @ {}'.format(self.ip)
        )
        self.server.connections.remove(self)
        self.conn.shutdown(socket.SHUT_WR)
        self.conn.close()
