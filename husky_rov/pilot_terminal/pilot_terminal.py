import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from gui import Ui_MainWindow
from tcp_client import TCPClient
from key_parsing import KeyParser


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        pilot_terminal = PilotTerminal()
        sys.exit(app.exec_())
    finally:
        pilot_terminal.quit_program()  # Graceful shutdown of socket & ROV


class PilotTerminal(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.connectButton.clicked.connect(self.connnect_to_rov)
        self.ui.disconnectButton.clicked.connect(self.disconnect_from_rov)
        self.setWindowIcon(QtGui.QIcon('../../images/husky.jpeg'))
        self.show()

        self.key_parser = KeyParser()
        self.client = TCPClient()
        self.client.listener.data_signal.connect(self.update_ui)
        self.timer = QTimer()  # Timer to get ROV status at random intervals
        self.timer.timeout.connect(self.get_rov_status)

    # Prints text to the control interface
    def print_to_window(self, message):
        self.ui.textBrowser.append(message)

    def connnect_to_rov(self):
        port = self.ui.portTextField.text()
        try:
            self.client.connect(port)
        except ValueError:
            self.print_to_window('Invalid port')
            return
        except ConnectionRefusedError:
            self.print_to_window('Connection refused by ROV')
            return
        except OverflowError:
            self.print_to_window('Port number out of range')
            return
        self.timer.start(50)  # Start timer at 20 Hz
        self.ui.portTextField.setDisabled(True)
        self.ui.connectButton.setDisabled(True)
        self.ui.disconnectButton.setDisabled(False)

    def disconnect_from_rov(self):
        self.client.disconnect()
        self.timer.stop()
        self.ui.portTextField.setDisabled(False)
        self.ui.connectButton.setDisabled(False)
        self.ui.disconnectButton.setDisabled(True)

    def get_rov_status(self):
        self.client.send('REQUEST_TELEMETRY')

    def update_ui(self, data):
        if data[0] == 'TELEMETRY':
            rov_status = data[1]
            self.ui.motorSlider_1.setValue(rov_status['motor_1_speed'])
            self.ui.motorSlider_2.setValue(rov_status['motor_2_speed'])
            self.ui.motorSlider_3.setValue(rov_status['motor_3_speed'])
            self.ui.motorSlider_4.setValue(rov_status['motor_4_speed'])
            self.ui.motorSlider_5.setValue(rov_status['motor_5_speed'])
            self.ui.motorSlider_6.setValue(rov_status['motor_6_speed'])
            self.ui.uMotorSlider.setValue(rov_status['u_motor_speed'])

            if rov_status['u_rov_deployed']:
                self.ui.uMotorSlider.setStyleSheet(
                    '''QSlider::handle:vertical:disabled
                    {background-color: rgb(0, 122, 217);}'''
                )
                self.ui.uRovStatus.setText('Released')
                self.ui.uRovStatus.setStyleSheet('color:rgb(180,0,0)')
            else:
                self.ui.uMotorSlider.setStyleSheet('')
                self.ui.uRovStatus.setText('Docked')
                self.ui.uRovStatus.setStyleSheet('color:rgb(0, 180, 0)')

            self.ui.sensitivitySlider.setValue(rov_status['speed_multiplier'])

            if rov_status['pilot_connected']:
                self.ui.pilotConnected.setStyleSheet('color:rgb(0, 180, 0)')
                self.ui.pilotConnected.setText('Connected')
            else:
                self.ui.pilotConnected.setStyleSheet('color:rgb(180, 0, 0)')
                self.ui.pilotConnected.setText('Not Connected')

            if rov_status['copilot_connected']:
                self.ui.copilotConnected.setStyleSheet('color:rgb(0, 180, 0)')
                self.ui.copilotConnected.setText('Connected')
            else:
                self.ui.copilotConnected.setStyleSheet('color:rgb(180, 0, 0)')
                self.ui.copilotConnected.setText('Not Connected')

            self.ui.hCamSlider.setValue(
                1500 - (rov_status['h_cam_servo_position'] - 1500)
            )
            self.ui.vCamSlider.setValue(
                1400 - (rov_status['v_cam_servo_position'] - 1400)
            )
        else:
            self.ui.textBrowser.append(data[1])

    def keyPressEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat():
            command = self.key_parser.parse_press(key)
            if command and self.client.is_connected:
                self.client.send(command)

    def keyReleaseEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat():
            command = self.key_parser.parse_release(key)
            if command and self.client.is_connected:
                self.client.send(command)

    def quit_program(self):
        if self.client.is_connected:
            self.client.disconnect()
        sys.exit()


if __name__ == '__main__':
    main()
