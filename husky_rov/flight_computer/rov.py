import pigpio
from components import Motor

class ROV:

    def __init__(self):
        self.urov = uROV(self)
        self.speed_multiplier = 3
        self.pilot_connected = False
        self.copilot_connected = False
        self.rpi = pigpio.pi()
        self.motor_1 = Motor(self, 5)
        self.motor_2 = Motor(self, 6)
        self.motor_3 = Motor(self, 13)
        self.motor_4 = Motor(self, 19)
        self.motor_5 = Motor(self, 26)
        self.motor_6 = Motor(self, 12)
        self.status = {
            'motor_1_speed' : 1500,
            'motor_2_speed' : 1500,
            'motor_3_speed' : 1500,
            'motor_4_speed' : 1500,
            'motor_5_speed' : 1500,
            'motor_6_speed' : 1500,
            'u_motor_speed' : 1500,
            'u_rov_deployed' : False,
            'speed_multiplier' : 3,
            'pilot_connected' : False,
            'copilot_connected' : False
        }
        self.commands = {
            'FORWARD' : self.go_forward,
            'BACKWARD' : self.go_backward,
            'STRAFE_LEFT' : self.strafe_left,
            'STRAFE_RIGHT' : self.strafe_right,
            'SPIN_LEFT' : self.spin_left,
            'SPIN_RIGHT' : self.spin_right,
            'UP' : self.go_up,
            'DOWN' : self.go_down,
            'U_FORWARD' : self.urov.go_forward,
            'U_BACKWARD' : self.urov.go_backward,
            'SET_SPEED_MULTIPLIER' : self.set_speed_multiplier,
            'U_TOGGLE_DEPLOY' : self.toggle_urov_deploy,
            'H_STOP' : self.h_stop,
            'V_STOP' : self.v_stop,
            'U_STOP' : self.urov.stop,
            'SHUT_DOWN' : self.shut_down,
            'REQUEST_TELEMETRY': self.send_status,
            'CONNECT_CLIENT' : self.connect_client,
            'DISCONNECT_CLIENT' : self.disconnect_client
        }

    def update_status(self):
        self.status['motor_1_speed'] = self.motor_1.speed
        self.status['motor_2_speed'] = self.motor_2.speed
        self.status['motor_3_speed'] = self.motor_3.speed
        self.status['motor_4_speed'] = self.motor_4.speed
        self.status['motor_5_speed'] = self.motor_5.speed
        self.status['motor_6_speed'] = self.motor_6.speed
        self.status['u_motor_speed'] = self.urov.motor.speed
        self.status['u_rov_deployed'] = self.urov.deployed
        self.status['speed_multiplier'] = self.speed_multiplier
        self.status['pilot_connected'] = self.pilot_connected
        self.status['copilot_connected'] = self.copilot_connected
        return self.status

    def go_forward(self):
        self.motor_1.thrust_forward()
        self.motor_2.thrust_forward()
        self.motor_3.thrust_forward()
        self.motor_4.thrust_forward()

    def go_backward(self):
        self.motor_1.thrust_backward()
        self.motor_2.thrust_backward()
        self.motor_3.thrust_backward()
        self.motor_4.thrust_backward()

    def strafe_left(self):
        self.motor_1.thrust_backward()
        self.motor_2.thrust_forward()
        self.motor_3.thrust_forward()
        self.motor_4.thrust_forward()

    def strafe_right(self):
        self.motor_1.thrust_forward()
        self.motor_2.thrust_backward()
        self.motor_3.thrust_backward()
        self.motor_4.thrust_backward()

    def spin_left(self):
        self.motor_1.thrust_forward()
        self.motor_2.thrust_backward()
        self.motor_3.thrust_backward()
        self.motor_4.thrust_forward()

    def spin_right(self):
        self.motor_1.thrust_backward()
        self.motor_2.thrust_forward()
        self.motor_3.thrust_forward()
        self.motor_4.thrust_backward()

    def h_stop(self):
        self.motor_1.thrust_stop()
        self.motor_2.thrust_stop()
        self.motor_3.thrust_stop()
        self.motor_4.thrust_stop()

    def go_up(self):
        self.motor_5.thrust_forward()
        self.motor_6.thrust_forward()

    def go_down(self):
        self.motor_5.thrust_backward()
        self.motor_6.thrust_backward()

    def v_stop(self):
        self.motor_5.thrust_stop()
        self.motor_6.thrust_stop()

    def set_speed_multiplier(self, command):
        multiplier = command[1]
        self.speed_multiplier = multiplier

    def shut_down(self):
        self.h_stop()
        self.v_stop()
        self.urov.stop()
        self.set_speed_multiplier((None, 3))
        self.urov.deployed = False
        self.motor_1.kill_pwm()
        self.motor_2.kill_pwm()
        self.motor_3.kill_pwm()
        self.motor_4.kill_pwm()
        self.motor_5.kill_pwm()
        self.motor_6.kill_pwm()
        self.urov.motor.kill_pwm()


    def toggle_urov_deploy(self):
        if self.urov.deployed:
            self.urov.deployed = False
        else:
            self.urov.deployed = True

    def connect_client(self, command):
        if command[1] == 'PILOT':
            self.pilot_connected = True
        else:
            self.copilot_connected = True

    def disconnect_client(self, command):
        if command[1] == 'PILOT':
            self.pilot_connected = False
        else:
            self.copilot_connected = False

    def send_status(self):
        pass

class uROV:

    def __init__(self, rov):
        self.motor = Motor(rov, 16)
        self.rov = rov
        self.deployed = False

    def go_forward(self):
        if self.deployed:
            self.motor.thrust_forward()

    def go_backward(self):
        if self.deployed:
            self.motor.thrust_backward()

    def stop(self):
        self.motor.thrust_stop()
