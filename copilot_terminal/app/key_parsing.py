from PyQt5.QtCore import Qt


class KeyParser:

    def __init__(self):
        # Associate PyQt keys with the 'command' to be sent to the ROV.
        # 'group' is to keep an array of the commands of related, currently-
        # pressed keys.
        self.movement_keys = {
            Qt.Key_W: {
                'command': ('MOVE_HORIZONTAL', 'FORWARD'),
                'group': 'horizontal_keys'
            },
            Qt.Key_S: {
                'command': ('MOVE_HORIZONTAL', 'BACKWARD'),
                'group': 'horizontal_keys'
            },
            Qt.Key_A: {
                'command': ('MOVE_HORIZONTAL', 'STRAFE_LEFT'),
                'group': 'horizontal_keys'
            },
            Qt.Key_D: {
                'command': ('MOVE_HORIZONTAL', 'STRAFE_RIGHT'),
                'group': 'horizontal_keys'
            },
            Qt.Key_J: {
                'command': ('MOVE_HORIZONTAL', 'SPIN_LEFT'),
                'group': 'horizontal_keys'
            },
            Qt.Key_L: {
                'command': ('MOVE_HORIZONTAL', 'SPIN_RIGHT'),
                'group': 'horizontal_keys'
            },
            Qt.Key_I: {
                'command': ('MOVE_VERTICAL', 'UP'),
                'group': 'vertical_keys'
            },
            Qt.Key_K: {
                'command': ('MOVE_VERTICAL', 'DOWN'),
                'group': 'vertical_keys'
            },
            Qt.Key_PageUp: {
                'command': ('MOVE_MICRO_ROV', 'FORWARD'),
                'group': 'micro_rov_keys'
            },
            Qt.Key_Up: {
                'command': ('MOVE_CAMERA_SERVO', 'CCW'),
                'group': 'cam_servo_keys'
            },
            Qt.Key_Down: {
                'command': ('MOVE_CAMERA_SERVO', 'CW'),
                'group': 'cam_servo_keys'
            },
            Qt.Key_Left: {
                'command': ('MOVE_CLAW_SERVO', 'CCW'),
                'group': 'claw_servo_keys'
            },
            Qt.Key_Right: {
                'command': ('MOVE_CLAW_SERVO', 'CW'),
                'group': 'claw_servo_keys'
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
                'command': 'TOGGLE_CLAW'
            },
            Qt.Key_Delete: {
                'command': 'TOGGLE_AIR'
            }
        }
        # List of commands for keys currently pressed. If no keys are pressed,
        # the "stop" command of that group remains the only elements in the
        # array.
        self.pressed_keys = {
            'horizontal_keys': [('MOVE_HORIZONTAL', 'STOP')],
            'vertical_keys': [('MOVE_VERTICAL', 'STOP')],
            'micro_rov_keys': [('MOVE_MICRO_ROV', 'STOP')],
            'cam_servo_keys': [('MOVE_CAMERA_SERVO', 'STOP')],
            'claw_servo_keys': [('MOVE_CLAW_SERVO', 'STOP')]
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
