# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '..\copilot_terminal\gui\qt\calculator_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(236, 143)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.r1Edit = QtWidgets.QLineEdit(Dialog)
        self.r1Edit.setObjectName("r1Edit")
        self.gridLayout.addWidget(self.r1Edit, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.videoLabel = QtWidgets.QLabel(Dialog)
        self.videoLabel.setText("")
        self.videoLabel.setObjectName("videoLabel")
        self.gridLayout.addWidget(self.videoLabel, 0, 2, 1, 1)
        self.r2Edit = QtWidgets.QLineEdit(Dialog)
        self.r2Edit.setObjectName("r2Edit")
        self.gridLayout.addWidget(self.r2Edit, 0, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.r3Edit = QtWidgets.QLineEdit(Dialog)
        self.r3Edit.setObjectName("r3Edit")
        self.gridLayout.addWidget(self.r3Edit, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lEdit = QtWidgets.QLineEdit(Dialog)
        self.lEdit.setObjectName("lEdit")
        self.gridLayout.addWidget(self.lEdit, 1, 4, 1, 1)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.volumeEdit = QtWidgets.QLineEdit(self.frame)
        self.volumeEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.volumeEdit.setObjectName("volumeEdit")
        self.gridLayout_2.addWidget(self.volumeEdit, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 1, 1, 1)
        self.submitButton = QtWidgets.QPushButton(self.frame)
        self.submitButton.setObjectName("submitButton")
        self.gridLayout_2.addWidget(self.submitButton, 0, 1, 1, 2)
        self.gridLayout.addWidget(self.frame, 2, 0, 1, 5)
        self.gridLayout.setRowStretch(0, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Calculator"))
        self.label_3.setText(_translate("Dialog", "R2:"))
        self.label_4.setText(_translate("Dialog", "L:"))
        self.label_2.setText(_translate("Dialog", "R1:"))
        self.label.setText(_translate("Dialog", "R3:"))
        self.label_5.setText(_translate("Dialog", "Volume:"))
        self.submitButton.setText(_translate("Dialog", "Submit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

