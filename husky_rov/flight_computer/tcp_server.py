import socket
from threading import Thread
import pickle
from rov import ROV

class TCPServer:

    def __init__(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, port))
        sock.listen(5)
        self.rov = ROV()
        self.connections = []
        while True:
            conn, addr = sock.accept()
            self.connections.append(conn)
            print('Client @ ' + str(addr) + ' has connected')
            self.send('MESSAGE', 'Connected to ROV @ 192.168.2.100')
            listener = Thread(target=self.listen, args=(conn, addr))
            listener.start()
            self.send_rov_status()

    def send(self, packet_type, data):
        data = pickle.dumps((packet_type, data))
        for connection in self.connections:
            connection.send(data)

    def listen(self, conn, addr):
        while True:
            command = conn.recv(2048)
            if not command:
                conn.close()
                self.connections.remove(conn)
                print('Client @: ' + str(addr) + ' has disconnected')
                break
            command = pickle.loads(command)
            if isinstance(command, tuple):
                function = self.rov.commands[command[0]]
                function(command)
            else:
                function = self.rov.commands[command]
                function()

            self.send_rov_status()

    def send_rov_status(self):
        status = self.rov.update_status()
        self.send('TELEMETRY', status)
