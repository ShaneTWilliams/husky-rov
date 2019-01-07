import socket
import pickle
from threading import Thread
from rov import ROV


class ROVServer:

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.rov = ROV()
        self.connections = []  # current connections to the rov
        self.listen_for_connections()

    # Listen for clients and instantiate a Connection object when one connects
    def listen_for_connections(self):
        self.sock.listen(5)
        while True:
            conn, addr = self.sock.accept()
            Connection(conn, addr, self)

    # Sends the rov's current status to all clients
    def send_telemetry(self):
        telemetry = self.rov.update_status()
        telemetry = pickle.dumps(('TELEMETRY', telemetry))
        for connection in self.connections:
            connection.conn.send(telemetry)

    # Sends a messsage to all clients
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
        self.listener.start()  # spawn threaded listener
        print('Client @ ' + addr[0] + ' has connected')
        self.server.send_message(
            'Client connected to ROV @ {}'.format(self.ip)
        )
        # TODO: move this shit somewhere else
        self.server.rov.v_cam_servo.move_to(self.server.rov.v_cam_servo.position)
        self.server.rov.h_cam_servo.move_to(self.server.rov.h_cam_servo.position)

    # Threaded function, listens on socket for commands
    def listen(self):
        while True:
            command = self.conn.recv(2048)
            if not command:
                self.disconnect()
                break
            command = pickle.loads(command)
            # If the command is a tuple, it contains arguments
            # These must be passed to the function associated with the command.
            # The zeroeth element will be the command, and subsequent elements
            # will be the arguments.
            if command != 'REQUEST_TELEMETRY':
                print(command)
            if isinstance(command, tuple):
                function = self.server.rov.commands[command[0]]
                function(command)
            # Else, the command contains no arguments and the function is
            # called outright.
            else:
                function = self.server.rov.commands[command]
                function()
            # After every command, telemetry is sent back to all clients
            self.server.send_telemetry()

    # Graceful shutdown of the socket
    def disconnect(self):
        print('Client @ ' + str(self.ip) + ' has disconnected')
        self.server.send_message(
            'Client disconnected from ROV @ {}'.format(self.ip)
        )
        self.server.connections.remove(self)
        self.conn.shutdown(socket.SHUT_WR)
        self.conn.close()
        if not self.server.rov.pilot_connected:
            self.server.rov.shut_down()
