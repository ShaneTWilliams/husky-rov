import time
import os
import glob
from threading import Thread

from sense_hat import SenseHat
import pigpio


class MicroROV:

    def __init__(self, rpi):
        self.relay = Relay(rpi, 17)

    def move(self, action):
        if action == 'FORWARD':
            self.relay.turn_on()
        elif action == 'STOP':
            self.relay.turn_off()


class Claw:
    def __init__(self, rpi, servo_pin, servo_bounds):
        self.servo = Servo(rpi, servo_pin, servo_bounds)
        self.is_closed = False

    def actuate(self):
        if self.is_closed:
            self.is_closed = False
        else:
            self.is_closed = True


class Motor:

    def __init__(self, rov, pin):
        self.rov = rov
        self.rpi = self.rov.rpi
        self.pin = pin
        self.rpi.set_mode(self.pin, pigpio.OUTPUT)
        self.speed = 1500  # All speeds are PWM pulse widths, in microseconds

    def thrust_forward(self):
        self.speed = 1500 + 40 * self.rov.speed_multiplier
        self.rpi.set_servo_pulsewidth(self.pin, self.speed)

    def thrust_backward(self):
        self.speed = 1500 - 40 * self.rov.speed_multiplier
        self.rpi.set_servo_pulsewidth(self.pin, self.speed)

    def thrust_stop(self):
        self.speed = 1500
        self.rpi.set_servo_pulsewidth(self.pin, self.speed)

    def kill_pwm(self):
        self.rpi.set_servo_pulsewidth(self.pin, 0)  # hold pwm line low


class Servo:

    def __init__(self, rpi, pin, bounds):
        self.rpi = rpi
        self.pin = pin
        self.bounds = bounds
        self.moving_clockwise = False
        self.moving_counterclockwise = False
        self.position = 1500
        self.rpi.set_mode(self.pin, pigpio.OUTPUT)
        self.move_to(self.position)
        self.timer = Thread(target=self.increment_position)
        self.timer.start()

    def increment_position(self):
        while True:
            if self.moving_clockwise and self.position < self.bounds[1]:
                self.position += 1
                self.move_to(self.position)
            elif (self.moving_counterclockwise
                  and self.position > self.bounds[0]):
                self.position -= 1
                self.move_to(self.position)
            time.sleep(0.002)

    def move(self, action):
        if action == 'CW':
            self.move_clockwise()
        elif action == 'CCW':
            self.move_counterclockwise()
        elif action == 'STOP':
            self.stop()

    def move_clockwise(self):
        self.moving_counterclockwise = False
        self.moving_clockwise = True

    def move_counterclockwise(self):
        self.moving_clockwise = False
        self.moving_counterclockwise = True

    def stop(self):
        self.moving_clockwise = False
        self.moving_counterclockwise = False

    def move_to(self, position):
        self.rpi.set_servo_pulsewidth(self.pin, position)

    def kill_pwm(self):
        self.rpi.set_servo_pulsewidth(self.pin, 0)  # hold pwm line low


class Relay:

    def __init__(self, rpi, pin):
        self.rpi = rpi
        self.pin = pin
        self.is_on = False

    def turn_on(self):
        self.rpi.write(self.pin, True)
        self.is_on = True

    def turn_off(self):
        self.rpi.write(self.pin, False)
        self.is_on = False


class SenseHat(SenseHat):

    def __init__(self):
        super().__init__()

    def get_can_temp_1(self):
        return round(self.get_temperature_from_humidity(), 2)

    def get_can_temp_2(self):
        return round(self.get_temperature_from_pressure(), 2)

    def get_can_humidity(self):
        return round(self.get_humidity(), 2)

    def get_can_pressure(self):
        return round(self.get_pressure(), 2)

    def get_pitch(self):
        orientation = self.get_orientation()
        pitch = orientation['pitch']
        if pitch > 0 and pitch < 90:
            pitch *= -1
        else:
            pitch = -1 * (pitch - 360)
        return round(pitch, 2)

    def get_roll(self):
        orientation = self.get_orientation()
        roll = orientation['roll']
        roll = -1 * (roll - 180)
        return round(roll, 2)


class WaterTempSensor:
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        try:
            device_folder = glob.glob(base_dir + '28*')[0]
            self.device_file = device_folder + '/w1_slave'
            self.is_connected = True
        except IndexError:
            self.is_connected = False

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        if not self.is_connected:
            return '---'
        lines = self.read_temp_raw()
        if lines[0].strip()[-3:] == 'YES':
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                return round(temp_c, 2)
        return
