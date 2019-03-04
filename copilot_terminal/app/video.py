from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal

from gui.python.video_dialog import Ui_Dialog
from app.computer_vision import VideoProcessor


class VideoDialog(QtWidgets.QDialog):

    key_press_signal = pyqtSignal(QtGui.QKeyEvent)
    key_release_signal = pyqtSignal(QtGui.QKeyEvent)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        circle = QtGui.QPixmap('images/circle.png')
        triangle = QtGui.QPixmap('images/triangle.png')
        line = QtGui.QPixmap('images/line.png')
        square = QtGui.QPixmap('images/square.png')
        self.ui.circleLabel.setPixmap(circle.scaledToWidth(80))
        self.ui.triangleLabel.setPixmap(triangle.scaledToWidth(80))
        self.ui.lineLabel.setPixmap(line.scaledToWidth(80))
        self.ui.squareLabel.setPixmap(square.scaledToWidth(80))

        self.show_binary_video = False
        self.processor = VideoProcessor()
        self.processor.video_signal.connect(self.update_video)
        self.processor.shape_signal.connect(self.update_shape_count)
        self.processor.start()

    def update_video(self, frame):
        frame = frame.scaledToWidth(1000)
        self.ui.videoLabel.setPixmap(frame)

    def update_shape_count(self, shapes):
        self.ui.circleCount.setText(str(shapes['circles']))
        self.ui.triangleCount.setText(str(shapes['triangles']))
        self.ui.lineCount.setText(str(shapes['lines']))
        self.ui.squareCount.setText(str(shapes['squares']))

    def keyPressEvent(self, event):
        key = event.key()
        if not event.isAutoRepeat():
            if key == Qt.Key_Return:
                self.processor.source.release()
                self.processor.terminate()
                self.close()
            elif key == Qt.Key_Backspace:
                self.processor.show_binary_video = \
                    not self.processor.show_binary_video
            else:
                self.key_press_signal.emit(event)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat():
            self.key_release_signal.emit(event)
