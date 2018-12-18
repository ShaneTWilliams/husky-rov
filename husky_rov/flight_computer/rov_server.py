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
        self.commands = {
            'FORWARD' : self.rov.go_forward,
            'BACKWARD' : self.rov.go_backward,
            'STRAFE_LEFT' : self.rov.strafe_left,
            'STRAFE_RIGHT' : self.rov.strafe_right,
            'SPIN_LEFT' : self.rov.spin_left,
            'SPIN_RIGHT' : self.rov.spin_right,
            'UP' : self.rov.go_up,
            'DOWN' : self.rov.go_down,
            'U_FORWARD' : self.rov.urov.go_forward,
            'U_BACKWARD' : self.rov.urov.go_backward,
            'SET_SPEED_MULTIPLIER' : self.rov.set_speed_multiplier,
            'U_TOGGLE_DEPLOY' : self.rov.toggle_urov_deploy,
            'H_STOP' : self.rov.h_stop,
            'V_STOP' : self.rov.v_stop,
            'U_STOP' : self.rov.urov.stop
        }
        while True:
            conn, addr = sock.accept()
            print('Client IP and port: ' + str(addr))
            listener = Thread(target=self.listen, args=(conn,))
            listener.start()

    def listen(self, conn):
        while True:
            command = conn.recv(2048)
            command = pickle.loads(command)
            if not command:
                break
            if isinstance(command, tuple):
                function = self.commands[command[0]]
                function(command)
            else:
                function = self.commands[command]
                function()
            status = self.rov.update_status()
            status = pickle.dumps(status)
            conn.send(status)

if __name__ == '__main__':
    ROVServer('192.168.2.100', int(sys.argv[1]))
