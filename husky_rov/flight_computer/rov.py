import pigpio
from components import Motor, Servo


class ROV:

    def __init__(self):
        self.urov = uROV(self)
        self.speed_multiplier = 3
        self.pilot_connected = False
        self.copilot_connected = False
        self.rpi = pigpio.pi()  # rpi object, used for PWM control
        self.motor_1 = Motor(self, 18)
        self.motor_2 = Motor(self, 6)
        self.motor_3 = Motor(self, 13)
        self.motor_4 = Motor(self, 19)
        self.motor_5 = Motor(self, 26)
        self.motor_6 = Motor(self, 12)
        self.v_cam_servo = Servo(self, 20, (1000, 1800))
        self.h_cam_servo = Servo(self, 21, (900, 2100))
        self.update_status()
        # Possible commands to be interpreted and their associated functions
        self.commands = {
            'FORWARD': self.go_forward,
            'BACKWARD': self.go_backward,
            'STRAFE_LEFT': self.strafe_left,
            'STRAFE_RIGHT': self.strafe_right,
            'SPIN_LEFT': self.spin_left,
            'SPIN_RIGHT': self.spin_right,
            'UP': self.go_up,
            'DOWN': self.go_down,
            'U_FORWARD': self.urov.go_forward,
            'U_BACKWARD': self.urov.go_backward,
            'SET_SPEED_MULTIPLIER': self.set_speed_multiplier,
            'U_TOGGLE_DEPLOY': self.toggle_urov_deploy,
            'H_STOP': self.h_stop,
            'V_STOP': self.v_stop,
            'U_STOP': self.urov.stop,
            'SHUT_DOWN': self.shut_down,
            'REQUEST_TELEMETRY': self.update_status,
            'CONNECT_CLIENT': self.connect_client,
            'DISCONNECT_CLIENT': self.disconnect_client,
            'CAMSERVO_UP': self.v_cam_servo.move_counterclockwise,
            'CAMSERVO_DOWN': self.v_cam_servo.move_clockwise,
            'CAMSERVO_LEFT': self.h_cam_servo.move_clockwise,
            'CAMSERVO_RIGHT': self.h_cam_servo.move_counterclockwise,
            'CAMSERVO_V_STOP': self.v_cam_servo.stop,
            'CAMSERVO_H_STOP': self.h_cam_servo.stop
        }

    # Get latest values for the ROV's status
    def update_status(self):
        self.status = {
            'motor_1_speed': self.motor_1.speed,
            'motor_2_speed': self.motor_2.speed,
            'motor_3_speed': self.motor_3.speed,
            'motor_4_speed': self.motor_4.speed,
            'motor_5_speed': self.motor_5.speed,
            'motor_6_speed': self.motor_6.speed,
            'u_motor_speed': self.urov.motor.speed,
            'u_rov_deployed': self.urov.deployed,
            'speed_multiplier': self.speed_multiplier,
            'pilot_connected': self.pilot_connected,
            'copilot_connected': self.copilot_connected,
            'v_cam_servo_position': self.v_cam_servo.position,
            'h_cam_servo_position': self.h_cam_servo.position,
        }
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
        self.v_cam_servo.kill_pwm()
        self.h_cam_servo.kill_pwm()

    def toggle_urov_deploy(self):
        self.urov.deployed = not self.urov.deployed

    # Update pilot_connected/copilot_connected flags
    def connect_client(self, command):
        if command[1] == 'PILOT':
            self.pilot_connected = True
        elif command[1] == 'COPILOT':
            self.copilot_connected = True

    # Update pilot_connected/copilot_connected flags
    def disconnect_client(self, command):
        if command[1] == 'PILOT':
            self.pilot_connected = False
        elif command[1] == 'COPILOT':
            self.copilot_connected = False


class uROV:

    def __init__(self, rov):
        self.motor = Motor(rov, 17)
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
