import sys
import socket
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from gui import Ui_MainWindow
from tcp_client import TCPClient
from computer_vision import VideoStream


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        copilot_terminal = CopilotTerminal()
        sys.exit(app.exec_())
    finally:
        copilot_terminal.quit_program()


class CopilotTerminal(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(
            '/Users/shane/Documents/Code/HuskyROV/images/husky.jpeg'
        ))
        self.show()

        self.client = TCPClient('192.168.2.99', sys.argv[1], self)
        self.client.listener.data_signal.connect(self.update_gui)

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_rov_status)
        self.timer.start(500)

        self.stream = VideoStream('http://192.168.2.99:8081')
        self.stream.video_signal.connect(self.update_video)
        self.stream.start()

    def update_video(self, video):
        color_video = video[0].scaledToWidth(500)
        binary_video = video[1].scaledToWidth(500)
        self.ui.label.setPixmap(color_video)
        self.ui.label_2.setPixmap(binary_video)
        print(video[2])

    def get_rov_status(self):
        self.client.send('REQUEST_TELEMETRY')

    def update_gui(self, data):
        if data[0] == 'MESSAGE':
            self.ui.textBrowser.append(data[1])
        else:
            pass

    def quit_program(self):
        self.client.send(('DISCONNECT_CLIENT', 'COPILOT'))
        self.client.sock.shutdown(socket.SHUT_WR)
        sys.exit()


if __name__ == '__main__':
    main()
