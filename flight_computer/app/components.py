import time
import os
import glob
from threading import Thread

from sense_hat import SenseHat
import pigpio


class MicroROV:

    def __init__(self, rpi):
        self.relay_1 = Relay(rpi, 13)
        self.relay_2 = Relay(rpi, 16)
        self.speed = 0

    def move(self, action):
        if action == 'FORWARD':
            self.relay_1.turn_on()
            self.relay_2.turn_off()
            self.speed = 1
        elif action == 'BACKWARD':
            self.relay_1.turn_off()
            self.relay_2.turn_on()
            self.speed = -1
        elif action == 'STOP':
            self.relay_1.turn_off()
            self.relay_2.turn_off()
            self.speed = 0

class Claw:

    def __init__(self, rpi, servo_pin, servo_bounds):
        self.servo = Servo(rpi, servo_pin, servo_bounds)
        self.is_closed = False

    def actuate(self):
        self.is_closed = not self.is_closed


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
        self.set_led(False, (255, 0, 0))
        self.blinker = Thread(target=self.blink_led)
        self.blinker.start()

    def set_led(self, blinking, color):
        self.color = color
        if blinking:
            self.led_blinking = True
        else:
            self.led_blinking = False

    def blink_led(self):
        while True:
            self.clear(self.color)
            time.sleep(.5)
            if self.led_blinking:
                self.clear((0, 0, 0))
            time.sleep(.5)


    def get_can_temp_1(self):
        return round(self.get_temperature_from_humidity(), 2)

    def get_can_temp_2(self):
        return round(self.get_temperature_from_pressure(), 2)

    def get_can_humidity(self):
        return round(self.get_humidity(), 2)

    def get_can_pressure(self):
        return round(self.get_pressure(), 2)

    def get_pitch(self):
        pitch = self.get_orientation()['pitch']
        if pitch < 90:
            pitch *= -1
        else:
            pitch = (pitch-360)*-1
        return round(pitch, 2)

    def get_roll(self):
        roll = self.get_orientation()['roll']
        if roll < 90:
            roll *= -1
        else:
            roll = (roll-360)*-1
        return round(roll, 2)


class WaterTempSensor:

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        self.temp = 0
        try:
            device_folder = glob.glob(base_dir + '28*')[0]
            self.device_file = device_folder + '/w1_slave'
            self.is_connected = True
        except IndexError:
            self.is_connected = False
            self.read_thread = Thread(target=self.read_temp)
            self.read_thread.start()

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        while True:
            time.sleep(1)
            if not self.is_connected:
                self.temp = '---'
                print('yo')
                continue
            lines = self.read_temp_raw()
            if lines[0].strip()[-3:] == 'YES':
                equals_pos = lines[1].find('t=')
                if equals_pos != -1:
                    temp_string = lines[1][equals_pos+2:]
                    temp_c = float(temp_string) / 1000.0
                    self.temp = round(temp_c, 2)
