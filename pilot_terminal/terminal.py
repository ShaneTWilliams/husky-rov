import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from gui.python.terminal_window import Ui_MainWindow
from app.tcp_client import TCPClient
from app.key_parsing import KeyParser
from app.video import VideoDialog


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
        self.setup_ui()
        self.show()

        self.key_parser = KeyParser()
        self.client = TCPClient()
        self.client.listener.data_signal.connect(self.update_ui)

    def setup_ui(self):
        self.ui.connectButton.clicked.connect(self.connnect_to_rov)
        self.ui.disconnectButton.clicked.connect(self.disconnect_from_rov)
        self.setWindowIcon(QtGui.QIcon('../../images/husky.jpeg'))

    def show_video_dialog(self):
        self.video_dialog = VideoDialog()

    # Prints text to the control interface
    def print_to_window(self, message):
        self.ui.textBrowser.append(message)

    def connnect_to_rov(self):
        port = self.ui.portLineEdit.text()
        ip = self.ui.ipLineEdit.text()
        connection_error = self.client.connect(port, ip)
        if connection_error:
            self.print_to_window(connection_error)
            return
        self.ui.pilotStatus.setDisabled(False)
        self.ui.copilotStatus.setDisabled(False)
        self.ui.pneumaticsStatus.setDisabled(False)
        self.ui.portLineEdit.setDisabled(True)
        self.ui.ipLineEdit.setDisabled(True)
        self.ui.connectButton.setDisabled(True)
        self.ui.disconnectButton.setDisabled(False)
        self.ui.clawStatus.setDisabled(False)
        self.ui.motor1Slider.setDisabled(False)
        self.ui.motor2Slider.setDisabled(False)
        self.ui.motor3Slider.setDisabled(False)
        self.ui.motor4Slider.setDisabled(False)
        self.ui.motor5Slider.setDisabled(False)
        self.ui.motor6Slider.setDisabled(False)
        self.ui.microMotorSlider.setDisabled(False)
        self.ui.cameraServoSlider.setDisabled(False)
        self.ui.waterTempValue.setDisabled(False)
        self.ui.canTemp1Value.setDisabled(False)
        self.ui.canTemp2Value.setDisabled(False)
        self.ui.humidityValue.setDisabled(False)
        self.ui.pressureValue.setDisabled(False)
        self.ui.pitchValue.setDisabled(False)
        self.ui.pitchSlider.setDisabled(False)
        self.ui.rollValue.setDisabled(False)
        self.ui.rollSlider.setDisabled(False)
        self.ui.clawServoSlider.setDisabled(False)
        self.ui.speedMultiplierSlider.setDisabled(False)

    def disconnect_from_rov(self):
        self.client.disconnect()
        self.ui.pilotStatus.setText('Not Connected')
        self.ui.copilotStatus.setText('Not Connected')
        self.ui.pneumaticsStatus.setText('Not Connected')
        self.ui.pilotStatus.setStyleSheet('color:rgb(0, 0, 0)')
        self.ui.copilotStatus.setStyleSheet('color:rgb(0, 0, 0)')
        self.ui.pneumaticsStatus.setStyleSheet('color:rgb(0, 0, 0)')
        self.ui.pilotStatus.setDisabled(True)
        self.ui.copilotStatus.setDisabled(True)
        self.ui.pneumaticsStatus.setDisabled(True)
        self.ui.portLineEdit.setDisabled(False)
        self.ui.ipLineEdit.setDisabled(False)
        self.ui.connectButton.setDisabled(False)
        self.ui.disconnectButton.setDisabled(True)
        self.ui.clawStatus.setDisabled(True)
        self.ui.clawStatus.setText('---')
        self.ui.clawStatus.setStyleSheet('color:rgb(0, 0, 0)')
        self.ui.motor1Slider.setDisabled(True)
        self.ui.motor2Slider.setDisabled(True)
        self.ui.motor3Slider.setDisabled(True)
        self.ui.motor4Slider.setDisabled(True)
        self.ui.motor5Slider.setDisabled(True)
        self.ui.motor6Slider.setDisabled(True)
        self.ui.microMotorSlider.setDisabled(True)
        self.ui.cameraServoSlider.setDisabled(True)
        self.ui.waterTempValue.setDisabled(True)
        self.ui.canTemp1Value.setDisabled(True)
        self.ui.canTemp2Value.setDisabled(True)
        self.ui.humidityValue.setDisabled(True)
        self.ui.pressureValue.setDisabled(True)
        self.ui.pitchValue.setDisabled(True)
        self.ui.pitchSlider.setDisabled(True)
        self.ui.rollValue.setDisabled(True)
        self.ui.rollSlider.setDisabled(True)
        self.ui.clawServoSlider.setDisabled(True)
        self.ui.speedMultiplierSlider.setDisabled(True)

    def get_rov_status(self):
        self.client.send('REQUEST_TELEMETRY')

    def update_ui(self, telemetry):
        self.ui.motor1Slider.setValue(telemetry['motors']['motor_1_speed'])
        self.ui.motor2Slider.setValue(telemetry['motors']['motor_2_speed'])
        self.ui.motor3Slider.setValue(telemetry['motors']['motor_3_speed'])
        self.ui.motor4Slider.setValue(telemetry['motors']['motor_4_speed'])
        self.ui.motor5Slider.setValue(telemetry['motors']['motor_5_speed'])
        self.ui.motor6Slider.setValue(telemetry['motors']['motor_6_speed'])
        self.ui.microMotorSlider.setValue(
            telemetry['motors']['micro_motor_state']
        )
        self.ui.cameraServoSlider.setValue(
            telemetry['camera']['camera_servo_position']
        )
        self.ui.clawServoSlider.setValue(
            telemetry['claw']['claw_servo_position']
        )
        self.ui.speedMultiplierSlider.setValue(
            telemetry['motors']['speed_multiplier']
        )
        if telemetry['network']['pilot_connected']:
            self.ui.pilotStatus.setText('Connected')
            self.ui.pilotStatus.setStyleSheet('color:rgb(0, 180, 0)')
        else:
            self.ui.pilotStatus.setText('Not Connected')
            self.ui.pilotStatus.setStyleSheet('color:rgb(180, 0, 0)')
        if telemetry['network']['copilot_connected']:
            self.ui.copilotStatus.setText('Connected')
            self.ui.copilotStatus.setStyleSheet('color:rgb(0, 180, 0)')
        else:
            self.ui.copilotStatus.setText('Not Connected')
            self.ui.copilotStatus.setStyleSheet('color:rgb(180, 0, 0)')
        if telemetry['network']['pneumatics_connected']:
            self.ui.pneumaticsStatus.setText('Connected')
            self.ui.pneumaticsStatus.setStyleSheet('color:rgb(0, 180, 0)')
        else:
            self.ui.pneumaticsStatus.setText('Not Connected')
            self.ui.pneumaticsStatus.setStyleSheet('color:rgb(180, 0, 0)')
        if telemetry['claw']['claw_closed']:
            self.ui.clawStatus.setText('Closed')
            self.ui.clawStatus.setStyleSheet('color:rgb(180, 0, 0)')
        else:
            self.ui.clawStatus.setText('Open')
            self.ui.clawStatus.setStyleSheet('color:rgb(0, 180, 0)')
        self.ui.canTemp1Value.setText(
            str(telemetry['sensor_data']['can_temperature_1'])
        )
        self.ui.canTemp2Value.setText(
            str(telemetry['sensor_data']['can_temperature_2'])
        )
        self.ui.humidityValue.setText(
            str(telemetry['sensor_data']['can_humidity'])
        )
        self.ui.pressureValue.setText(
            str(telemetry['sensor_data']['can_pressure'])
        )
        self.ui.pitchValue.setText(str(telemetry['sensor_data']['pitch']))
        self.ui.pitchSlider.setValue(telemetry['sensor_data']['pitch'])
        self.ui.rollValue.setText(str(telemetry['sensor_data']['roll']))
        self.ui.rollSlider.setValue(telemetry['sensor_data']['roll'])

    def keyPressEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat():
            if key == QtCore.Qt.Key_Enter:
                self.show_video_dialog()
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
