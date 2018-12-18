class Motor:

    def __init__(self, rov):
        self.rov = rov
        self.forward = 1620
        self.backward = 1380
        self.stop = 1500
        self.speed = self.stop

    def update_speeds(self):
        self.forward = 1500 + 40 * self.rov.speed_multiplier
        self.backward = 1500 - 40 * self.rov.speed_multiplier

    def thrust_forward(self):
        self.update_speeds()
        self.speed = self.forward

    def thrust_backward(self):
        self.update_speeds()
        self.speed = self.backward

    def thrust_stop(self):
        self.speed = self.stop
