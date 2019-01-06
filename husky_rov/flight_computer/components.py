import time
from threading import Thread


class Motor:

    def __init__(self, rov, pin):
        self.rov = rov
        self.pin = pin
        self.speed = 1500  # All speeds are PWM pulse widths, in microseconds

    def thrust_forward(self):
        self.speed = 1500 + 40 * self.rov.speed_multiplier
        self.rov.rpi.set_servo_pulsewidth(self.pin, self.speed)

    def thrust_backward(self):
        self.speed = 1500 - 40 * self.rov.speed_multiplier
        self.rov.rpi.set_servo_pulsewidth(self.pin, self.speed)

    def thrust_stop(self):
        self.speed = 1500
        self.rov.rpi.set_servo_pulsewidth(self.pin, self.speed)

    def kill_pwm(self):
        self.rov.rpi.set_servo_pulsewidth(self.pin, 0)  # hold pwm line low


class Servo:

    def __init__(self, rov, pin, bounds):
        self.rov = rov
        self.pin = pin
        self.bounds = bounds
        self.position = 1500
        self.move(self.position)
        self.moving_clockwise = False
        self.moving_counterclockwise = False
        self.timer = Thread(target=self.increment_position)
        self.timer.start()

    def increment_position(self):
        while True:
            if self.moving_clockwise and self.position < self.bounds[1]:
                self.position += 1
                self.move(self.position)
            elif (self.moving_counterclockwise
                  and self.position > self.bounds[0]):
                self.position -= 1
                self.move(self.position)
            time.sleep(0.002)

    def move_clockwise(self):
        self.moving_counterclockwise = False
        self.moving_clockwise = True

    def move_counterclockwise(self):
        self.moving_clockwise = False
        self.moving_counterclockwise = True

    def stop(self):
        self.moving_clockwise = False
        self.moving_counterclockwise = False

    def move(self, position):
        self.rov.rpi.set_servo_pulsewidth(self.pin, position)

    def kill_pwm(self):
        self.rov.rpi.set_servo_pulsewidth(self.pin, 0)  # hold pwm line low
