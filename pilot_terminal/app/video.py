import cv2
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

from gui.python.video_dialog import Ui_Dialog


class VideoDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()
        self.processor = VideoProcessor()
        self.processor.video_signal.connect(self.update_video)
        self.processor.start()

    def update_video(self, frame):
        frame = frame.scaledToWidth(1000)
        self.ui.videoLabel.setPixmap(frame)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter:
            self.processor.source.release()
            self.processor.terminate()
            self.close()


class VideoProcessor(QThread):

    video_signal = pyqtSignal(QPixmap)

    def __init__(self):
        QThread.__init__(self)
        self.source = cv2.VideoCapture('http://192.168.2.99:8081')

    def run(self):
        while True:
            frame = self.grab_frame()
            frame = self.convert_to_qpixmap(frame)
            self.video_signal.emit(frame)

    def grab_frame(self):
        img_valid, frame = self.source.read()
        if img_valid:
            return frame

    def convert_to_qpixmap(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = width * 3
        frame = QImage(
            frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888
        )
        frame = QPixmap.fromImage(frame)
        return frame
