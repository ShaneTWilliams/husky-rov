from PyQt5.QtCore import Qt

class Key:

    def __init__(self, value, key_type, group, func, cur_list, rest_func):
        self.value = value
        self.key_type = key_type
        self.group = group
        self.func = func
        self.rest_func = rest_func
        self.num_literals = {
            Qt.Key_1 : 1,
            Qt.Key_2 : 2,
            Qt.Key_3 : 3,
            Qt.Key_4 : 4,
            Qt.Key_5 : 5
        }
        self.cur_list = cur_list

    def on_press(self):
        if self.key_type == 'MOVEMENT_KEY':
            self.cur_list.append(self)
            self.func()
        else:
            if self.group == 'NUM_KEYS':
                self.func(self.num_literals[self.value])
            else:
                self.func()

    def on_release(self):
        if self.key_type == 'MOVEMENT_KEY':
            self.cur_list.remove(self)
            if self.cur_list:
                self.cur_list[-1].func()
            else:
                self.rest_func()

class KeyFactory:

    def __init__(self, control):
        self.control = control
        self.rov = control.rov

        self.movement_keys = {
            'H_KEYS' : ({
                Qt.Key_W : self.rov.go_forward,
                Qt.Key_S : self.rov.go_backward,
                Qt.Key_A : self.rov.strafe_left,
                Qt.Key_D : self.rov.strafe_right,
                Qt.Key_J : self.rov.spin_left,
                Qt.Key_L : self.rov.spin_right,
            }, self.rov.h_stop),
            'V_KEYS' : ({
                Qt.Key_I : self.rov.go_up,
                Qt.Key_K : self.rov.go_down,
            }, self.rov.v_stop),
        }
        self.toggle_keys = {
            'NUM_KEYS' : {
                Qt.Key_1 : self.rov.set_speed_multiplier,
                Qt.Key_2 : self.rov.set_speed_multiplier,
                Qt.Key_3 : self.rov.set_speed_multiplier,
                Qt.Key_4 : self.rov.set_speed_multiplier,
                Qt.Key_5 : self.rov.set_speed_multiplier
            },
            'EXIT_KEYS' : {
                Qt.Key_Escape : self.control.quit_program
            }
        }
        self.keys = {}
        self.cur_lists = {}
        for group in self.movement_keys:
            self.cur_lists[group] = []

    def create_cur_lists(self):
        self.cur_lists = {}
        for group in self.movement_keys:
            self.cur_lists[group] = []

    def create_keys(self):
        for group in self.movement_keys:
            for key, func in self.movement_keys[group][0].items():
                self.keys[key] = Key(
                    key, 'MOVEMENT_KEY', group, func, self.cur_lists[group],
                    self.movement_keys[group][1]
                )
        for group in self.toggle_keys:
            for key, func in self.toggle_keys[group].items():
                self.keys[key] = Key(
                    key, 'TOGGLE_KEY', group, func, None, None
                )
        return self.keys
