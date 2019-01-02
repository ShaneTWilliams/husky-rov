class Motor:

    def __init__(self, rov, pin):
        self.rov = rov
        self.pin = pin  # pwm pin for motor's ESC
        self.speed = 1500  # all speeds are pwm pulse widths, in microseconds

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
