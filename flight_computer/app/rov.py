import threading
import time

import pigpio

from app.tcp_server import TCPServer
from app.components import (MicroROV, Claw, Motor, Servo, SenseHat,
                            WaterTempSensor)


class ROV:

    def __init__(self, ip, port):
        self.server = TCPServer(ip, port)
        self.init_hardware()
        self.control_loop()

    def init_hardware(self):
        self.rpi = pigpio.pi()  # rpi object, used for GPIO control
        self.micro_rov = MicroROV(self.rpi)
        self.speed_multiplier = 3
        self.pilot_connected = False
        self.copilot_connected = False
        self.pneumatics_connected = False
        self.motor_1 = Motor(self, 17)
        self.motor_2 = Motor(self, 6)
        self.motor_3 = Motor(self, 13)
        self.motor_4 = Motor(self, 19)
        self.motor_5 = Motor(self, 26)
        self.motor_6 = Motor(self, 12)
        self.camera_servo = Servo(self.rpi, 20, (1000, 1800))
        self.claw = Claw(self.rpi, 21, (1000, 1800))
        self.sense_hat = SenseHat()
        self.water_temp_sensor = WaterTempSensor()

    def stream_telemetry(self):
        while True:
            self.server.send_telemetry(self.update_status())
            time.sleep(.1)

    def control_loop(self):
        # Possible commands to be interpreted and their associated functions
        self.commands = {
            'MOVE_HORIZONTAL': self.move_horizontal,
            'MOVE_VERTICAL': self.move_vertical,
            'MOVE_MICRO_ROV': self.micro_rov.move,
            'SET_SPEED_MULTIPLIER': self.set_speed_multiplier,
            'SHUT_DOWN': self.shut_down,
            'REQUEST_TELEMETRY': self.update_status,
            'CONNECT_CLIENT': self.connect_client,
            'DISCONNECT_CLIENT': self.disconnect_client,
            'MOVE_CAMERA_SERVO': self.camera_servo.move,
            'MOVE_CLAW_SERVO': self.claw.servo.move,
            'TOGGLE_CLAW': self.claw.actuate
        }
        telemetry_streamer = threading.Thread(target=self.stream_telemetry)
        telemetry_streamer.start()
        while True:
            command = self.server.queued_commands.get()
            if command != 'REQUEST_TELEMETRY':
                print(command)
            if isinstance(command, tuple):
                function = self.commands[command[0]]
                function(command[1])
            else:
                function = self.commands[command]
                function()
            self.server.send_telemetry(self.update_status())

    # Get latest values for the ROV's status
    def update_status(self):
        return {
            'motors': {
                'motor_1_speed': self.motor_1.speed,
                'motor_2_speed': self.motor_2.speed,
                'motor_3_speed': self.motor_3.speed,
                'motor_4_speed': self.motor_4.speed,
                'motor_5_speed': self.motor_5.speed,
                'motor_6_speed': self.motor_6.speed,
                'micro_motor_state': self.micro_rov.relay.is_on,
                'speed_multiplier': self.speed_multiplier
            },
            'network': {
                'pilot_connected': self.pilot_connected,
                'copilot_connected': self.copilot_connected,
                'pneumatics_connected': self.pneumatics_connected
            },
            'camera': {
                'camera_servo_position': self.camera_servo.position
            },
            'claw': {
                'claw_servo_position': self.claw.servo.position,
                'claw_closed': self.claw.is_closed,
            },
            'sensors': {
                'can_temperature_1': self.sense_hat.get_can_temp_1(),
                'can_temperature_2': self.sense_hat.get_can_temp_1(),
                'can_pressure': self.sense_hat.get_can_pressure(),
                'can_humidity': self.sense_hat.get_can_humidity(),
                'pitch': self.sense_hat.get_pitch(),
                'roll': self.sense_hat.get_roll(),
                'water_temp': self.water_temp_sensor.read_temp()
            }
        }

    def move_horizontal(self, action):
        if action == 'FORWARD':
            self.motor_1.thrust_forward()
            self.motor_2.thrust_forward()
            self.motor_3.thrust_forward()
            self.motor_4.thrust_forward()
        elif action == 'BACKWARD':
            self.motor_1.thrust_backward()
            self.motor_2.thrust_backward()
            self.motor_3.thrust_backward()
            self.motor_4.thrust_backward()
        elif action == 'STRAFE_LEFT':
            self.motor_1.thrust_backward()
            self.motor_2.thrust_forward()
            self.motor_3.thrust_forward()
            self.motor_4.thrust_forward()
        elif action == 'STRAFE_RIGHT':
            self.motor_1.thrust_forward()
            self.motor_2.thrust_backward()
            self.motor_3.thrust_backward()
            self.motor_4.thrust_backward()
        elif action == 'SPIN_LEFT':
            self.motor_1.thrust_forward()
            self.motor_2.thrust_backward()
            self.motor_3.thrust_backward()
            self.motor_4.thrust_forward()
        elif action == 'SPIN_RIGHT':
            self.motor_1.thrust_backward()
            self.motor_2.thrust_forward()
            self.motor_3.thrust_forward()
            self.motor_4.thrust_backward()
        elif action == 'STOP':
            self.motor_1.thrust_stop()
            self.motor_2.thrust_stop()
            self.motor_3.thrust_stop()
            self.motor_4.thrust_stop()

    def move_vertical(self, action):
        if action == 'UP':
            self.motor_5.thrust_forward()
            self.motor_6.thrust_forward()
        elif action == 'DOWN':
            self.motor_5.thrust_backward()
            self.motor_6.thrust_backward()
        elif action == 'STOP':
            self.motor_5.thrust_stop()
            self.motor_6.thrust_stop()

    def set_speed_multiplier(self, value):
        self.speed_multiplier = value

    def shut_down(self):
        self.move_horizontal('STOP')
        self.move_vertical('STOP')
        self.micro_rov.move('STOP')
        self.motor_1.kill_pwm()
        self.motor_2.kill_pwm()
        self.motor_3.kill_pwm()
        self.motor_4.kill_pwm()
        self.motor_5.kill_pwm()
        self.motor_6.kill_pwm()
        self.camera_servo.kill_pwm()
        self.claw.servo.kill_pwm()

    # Update current server connections
    def connect_client(self, client):
        if client == 'PILOT':
            self.pilot_connected = True
        elif client == 'COPILOT':
            self.copilot_connected = True
        elif client == 'PNEUMATICS':
            self.pneumatics_connected = True

    # Update current server connections
    def disconnect_client(self, client):
        if client == 'PILOT':
            self.pilot_connected = False
        elif client == 'COPILOT':
            self.copilot_connected = False
        elif client == 'PNEUMATICS':
            self.pneumatics_connected = False
        if not (self.pilot_connected or self.copilot_connected):
            self.shut_down()
