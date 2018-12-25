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
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(
                '/Users/shane/Documents/Code/HuskyROV/images/husky.jpeg'
        ))
        self.show()
        self.client = TCPClient('192.168.2.100', sys.argv[1], self)
        self.client.listener.data_signal.connect(self.update_gui)
        self.key_parser = KeyParser()
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_rov_status)
        self.timer.start(500)

    def get_rov_status(self):
        self.client.send('REQUEST_TELEMETRY')

    def update_gui(self, data):
        if data[0] == 'MESSAGE':
            self.gui.textBrowser.append(data[1])
        else:
            rov_status = data[1]
            self.gui.motorSlider_1.setValue(rov_status['motor_1_speed'])
            self.gui.motorSlider_2.setValue(rov_status['motor_2_speed'])
            self.gui.motorSlider_3.setValue(rov_status['motor_3_speed'])
            self.gui.motorSlider_4.setValue(rov_status['motor_4_speed'])
            self.gui.motorSlider_5.setValue(rov_status['motor_5_speed'])
            self.gui.motorSlider_6.setValue(rov_status['motor_6_speed'])
            self.gui.uMotorSlider.setValue(rov_status['u_motor_speed'])

            if rov_status['u_rov_deployed']:
                self.gui.uMotorSlider.setStyleSheet(
                    '''QSlider::handle:vertical:disabled
                    {background-color: rgb(0, 122, 217);}'''
                )
                self.gui.uRovStatus.setText('Released')
                self.gui.uRovStatus.setStyleSheet('color:rgb(180,0,0)')
            else:
                self.gui.uMotorSlider.setStyleSheet('')
                self.gui.uRovStatus.setText('Docked')
                self.gui.uRovStatus.setStyleSheet('color:rgb(0, 180, 0)')
            self.gui.sensitivitySlider.setValue(rov_status['speed_multiplier'])

            if rov_status['pilot_connected']:
                self.gui.pilotConnected.setStyleSheet('color:rgb(0, 180, 0)')
                self.gui.pilotConnected.setText('Connected')
            else:
                self.gui.pilotConnected.setStyleSheet('color:rgb(180, 0, 0)')
                self.gui.pilotConnected.setText('Not Connected')

            if rov_status['copilot_connected']:
                self.gui.copilotConnected.setStyleSheet('color:rgb(0, 180, 0)')
                self.gui.copilotConnected.setText('Connected')
            else:
                self.gui.copilotConnected.setStyleSheet('color:rgb(180, 0, 0)')
                self.gui.copilotConnected.setText('Not Connected')

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
