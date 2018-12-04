from components import Motor

class ROV:

    def __init__(self, gui):
        self.gui = gui
        self.set_speed_multiplier(3)
        self.motor_1 = Motor(self, gui.motorSlider_1)
        self.motor_2 = Motor(self, gui.motorSlider_2)
        self.motor_3 = Motor(self, gui.motorSlider_3)
        self.motor_4 = Motor(self, gui.motorSlider_4)
        self.motor_5 = Motor(self, gui.motorSlider_5)
        self.motor_6 = Motor(self, gui.motorSlider_6)

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

    def set_speed_multiplier(self, multiplier):
        self.gui.sensitivitySlider.setValue(multiplier)
        self.speed_multiplier = multiplier

    def shut_down(self):
        self.h_stop()
        self.v_stop()
