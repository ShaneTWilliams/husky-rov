from PyQt5.QtCore import Qt


class KeyParser:

    def __init__(self):
        # Associate Qt keys with the 'command' to be sent to the ROV.
        # 'group' is to keep an array of the commands of related currently
        # pressed keys.
        # e.g. if you press 's', press 'w', then lift 'w', the command
        # associated with s will execute.
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
            Qt.Key_Up: {
                'command': 'CAMSERVO_UP',
                'group': 'CAMSERVO_V_KEYS'
            },
            Qt.Key_Down: {
                'command': 'CAMSERVO_DOWN',
                'group': 'CAMSERVO_V_KEYS'
            },
            Qt.Key_Left: {
                'command': 'CAMSERVO_LEFT',
                'group': 'CAMSERVO_H_KEYS'
            },
            Qt.Key_Right: {
                'command': 'CAMSERVO_RIGHT',
                'group': 'CAMSERVO_H_KEYS'
            },
        }
        # Toggle keys are one-time, they don't need to be associated with a
        # group or a "currently pressed" array.
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
        # List of commands for keys currently pressed. If no keys are pressed,
        # the "stop" commands of that group remain the only elements in the
        # array.
        self.pressed_keys = {
            'H_KEYS': ['H_STOP'],
            'V_KEYS': ['V_STOP'],
            'U_KEYS': ['U_STOP'],
            'CAMSERVO_H_KEYS': ['CAMSERVO_H_STOP'],
            'CAMSERVO_V_KEYS': ['CAMSERVO_V_STOP']
        }

    # Returns a command to be sent to the ROV based on currently pressed keys
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

    # Returns a command to be sent to the ROV based on currently pressed keys
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
