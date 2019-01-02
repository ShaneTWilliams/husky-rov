from PyQt5.QtCore import Qt


class KeyParser:

    def __init__(self):
        self.movement_keys = {
            Qt.Key_W: {
                'command': 'FORWARD',
                'group': 'H_KEYS'
            },
            Qt.Key_S: {
                'command': 'BACKWARD',
                'group': 'H_KEYS'
            },
            Qt.Key_A: {
                'command': 'STRAFE_LEFT',
                'group': 'H_KEYS'
            },
            Qt.Key_D: {
                'command': 'STRAFE_RIGHT',
                'group': 'H_KEYS'
            },
            Qt.Key_J: {
                'command': 'SPIN_LEFT',
                'group': 'H_KEYS'
            },
            Qt.Key_L: {
                'command': 'SPIN_RIGHT',
                'group': 'H_KEYS'
            },
            Qt.Key_I: {
                'command': 'UP',
                'group': 'V_KEYS'
            },
            Qt.Key_K: {
                'command': 'DOWN',
                'group': 'V_KEYS'
            },
            Qt.Key_PageUp: {
                'command': 'U_FORWARD',
                'group': 'U_KEYS'
            },
            Qt.Key_PageDown: {
                'command': 'U_BACKWARD',
                'group': 'U_KEYS'
            },

        }
        self.toggle_keys = {
            Qt.Key_1: {
                'command': ('SET_SPEED_MULTIPLIER', 1)
            },
            Qt.Key_2: {
                'command': ('SET_SPEED_MULTIPLIER', 2)
            },
            Qt.Key_3: {
                'command': ('SET_SPEED_MULTIPLIER', 3)
            },
            Qt.Key_4: {
                'command': ('SET_SPEED_MULTIPLIER', 4)
            },
            Qt.Key_5: {
                'command': ('SET_SPEED_MULTIPLIER', 5)
            },
            Qt.Key_Space: {
                'command': 'U_TOGGLE_DEPLOY'
            }
        }
        self.pressed_keys = {
            'H_KEYS': ['H_STOP'],
            'V_KEYS': ['V_STOP'],
            'U_KEYS': ['U_STOP']
        }

    def parse_press(self, key):
        if key in self.movement_keys:
            group = self.movement_keys[key]['group']
            command = self.movement_keys[key]['command']
            self.pressed_keys[group].append(command)
        elif key in self.toggle_keys:
            command = self.toggle_keys[key]['command']
        else:
            command = None
        return command

    def parse_release(self, key):
        if key in self.movement_keys:
            group = self.movement_keys[key]['group']
            command = self.movement_keys[key]['command']
            if command in self.pressed_keys[group]:
                self.pressed_keys[group].remove(command)
            command = self.pressed_keys[group][-1]
        else:
            command = None
        return command
