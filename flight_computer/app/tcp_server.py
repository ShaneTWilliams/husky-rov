import socket
import pickle
import queue
import threading


class TCPServer:

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.clients = []  # current connections to the server
        self.queued_commands = queue.Queue()
        self.listener = threading.Thread(target=self.listen_for_connections)
        self.listener.start()

    # Listen for clients and instantiate a Connection object when one connects
    def listen_for_connections(self):
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            client = Client(conn, addr, self)
            client.start()
            self.clients.append(client)

    # Sends the rov's current status to all clients
    def send_telemetry(self, telemetry):
        telemetry = pickle.dumps(telemetry)
        for client in self.clients:
            client.conn.send(telemetry)


class Client(threading.Thread):

    def __init__(self, conn, addr, server):
        self.conn = conn
        self.ip = addr[0]
        self.port = addr[1]
        self.server = server
        threading.Thread.__init__(self)

    # Threaded function, listens on socket for commands
    def run(self):
        while True:
            try:
                command = self.conn.recv(2048)
            except ConnectionResetError:
                self.disconnect()
                break
            if not command:
                self.disconnect()
                break
            command = pickle.loads(command)
            self.server.queued_commands.put(command)

    # Graceful shutdown of the socket
    def disconnect(self):
        self.server.clients.remove(self)
        self.conn.close()
