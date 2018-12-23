from PyQt5 import QtWidgets
import sys
import socket
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
        self.show()
        self.client = TCPClient('192.168.2.100', sys.argv[1], self)

    def update_gui(self, rov_status):
        pass

    def keyPressEvent(self, event):
        pass

    def keyReleaseEvent(self, event):
        pass

    def quit_program(self):
        self.client.sock.shutdown(socket.SHUT_WR)
        sys.exit()

if __name__ == '__main__':
    main()
