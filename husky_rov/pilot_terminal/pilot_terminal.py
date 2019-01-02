import sys
import socket
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
        pilot_terminal.quit_program()


class PilotTerminal(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(
                '/Users/shane/Documents/Code/HuskyROV/images/husky.jpeg'
        ))
        self.show()
        self.client = TCPClient('192.168.2.99', sys.argv[1], self)
        self.client.listener.data_signal.connect(self.update_ui)
        self.key_parser = KeyParser()
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_rov_status)
        self.timer.start(500)

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
        else:
            self.ui.textBrowser.append(data[1])

    def keyPressEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat():
            command = self.key_parser.parse_press(key)
            if command:
                self.client.send(command)

    def keyReleaseEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat():
            command = self.key_parser.parse_release(key)
            if command:
                self.client.send(command)

    def quit_program(self):
        self.client.send(('DISCONNECT_CLIENT', 'PILOT'))
        self.client.sock.shutdown(socket.SHUT_WR)
        sys.exit()


if __name__ == '__main__':
    main()
