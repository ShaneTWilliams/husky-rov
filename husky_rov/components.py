class Motor:

    def __init__(self, rov, slider):
        self.rov = rov
        self.slider = slider

    def update_speeds(self):
        self.forward = 1500 + 40 * self.rov.speed_multiplier
        self.backward = 1500 - 40 * self.rov.speed_multiplier
        self.stop = 1500

    def thrust_forward(self):
        self.update_speeds()
        self.slider.setValue(self.forward)

    def thrust_backward(self):
        self.update_speeds()
        self.slider.setValue(self.backward)

    def thrust_stop(self):
        self.update_speeds()
        self.slider.setValue(self.stop)
