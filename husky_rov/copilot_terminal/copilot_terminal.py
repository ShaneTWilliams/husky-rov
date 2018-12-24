import sys
import socket
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from gui import Ui_MainWindow
from tcp_client import TCPClient

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
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(r'C:\Users\shane\Documents\Code\HuskyROV\images\husky.jpeg'))
        self.show()
        self.client = TCPClient('192.168.2.100', sys.argv[1], self)
        self.client.listener.data_signal.connect(self.update_gui)
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_rov_status)
        self.timer.start(500)

    def get_rov_status(self):
        self.client.send('REQUEST_TELEMETRY')

    def update_gui(self, data):
        if data[0] == 'MESSAGE':
            self.gui.textBrowser.append(data[1])
        else:
            pass

    def quit_program(self):
        self.client.send(('DISCONNECT_CLIENT', 'COPILOT'))
        self.client.sock.shutdown(socket.SHUT_WR)
        sys.exit()

if __name__ == '__main__':
    main()
