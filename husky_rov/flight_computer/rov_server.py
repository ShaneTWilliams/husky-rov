import socket
import sys
from threading import Thread
import pickle
from rov import ROV

class ROVServer:

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
            listener = Thread(target=self.listen, args=(conn, addr))
            listener.start()
            status = self.rov.update_status()
            status = pickle.dumps(status)
            conn.send(status)

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

            status = self.rov.update_status()
            status = pickle.dumps(status)
            for connection in self.connections:
                connection.send(status)

if __name__ == '__main__':
    ROVServer('192.168.2.100', int(sys.argv[1]))
