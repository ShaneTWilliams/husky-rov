from components import Motor

class ROV:

    def __init__(self):
        self.urov = uROV(self)
        self.speed_multiplier = 3
        self.motor_1 = Motor(self)
        self.motor_2 = Motor(self)
        self.motor_3 = Motor(self)
        self.motor_4 = Motor(self)
        self.motor_5 = Motor(self)
        self.motor_6 = Motor(self)
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

    def toggle_urov_deploy(self):
        if self.urov.deployed:
            self.urov.deployed = False
        else:
            self.urov.deployed = True


class uROV:

    def __init__(self, rov):
        self.motor = Motor(rov)
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
