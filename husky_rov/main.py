from PyQt5 import QtWidgets
import sys

from gui import Ui_MainWindow
from key_parsing import KeyFactory
from rov import ROV


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        main_control = MainControl()
        sys.exit(app.exec_())
    finally:
        main_control.quit_program()

class MainControl(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        self.show()

        self.rov = ROV(self.gui)
        key_factory = KeyFactory(self)
        self.keys = key_factory.create_keys()

    def keyPressEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat() and key in self.keys:
            self.keys[key].on_press()

    def keyReleaseEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat() and key in self.keys:
            self.keys[key].on_release()

    def quit_program(self):
        self.rov.shut_down()
        sys.exit()


if __name__ == '__main__':
    main()
