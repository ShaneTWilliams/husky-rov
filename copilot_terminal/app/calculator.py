import math

from PyQt5 import QtWidgets

from gui.python.calculator_dialog import Ui_Dialog


class CalculatorDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.submitButton.clicked.connect(self.calculate_volume)

    def calculate_volume(self):
        try:
            r1 = float(self.ui.r1Edit.text())
            r2 = float(self.ui.r2Edit.text())
            r3 = float(self.ui.r3Edit.text())
            length = float(self.ui.lEdit.text())
        except ValueError:
            self.ui.volumeEdit.setText('Invalid Input')
            return
        volume = (math.pi*length/3)*((r3**2)+(r1*r3)+(r1**2)-(3*r2**2))
        volume = round(volume, 2)
        self.ui.volumeEdit.setText(str(volume))
