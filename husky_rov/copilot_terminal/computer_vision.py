import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class VideoStream(QThread):

    video_signal = pyqtSignal(tuple)

    def __init__(self, ip):
        QThread.__init__(self)
        self.source = cv2.VideoCapture(ip)
        self.processor = VideoProcessor()

    def grab_frame(self):
        img_valid, brg_frame = self.source.read()
        if img_valid:
            rgb_frame = cv2.cvtColor(brg_frame, cv2.COLOR_BGR2RGB)
            return rgb_frame

    def process_frame(self):
        frame = self.grab_frame()
        q_frame = self.processor.convert_to_qpixmap(frame)
        binary_frame, contours = self.processor.make_binary(frame)
        q_binary_frame = self.processor.convert_to_qpixmap(binary_frame)
        shapes = self.processor.find_shapes(contours)
        return q_frame, q_binary_frame, shapes

    def run(self):
        while True:
            self.video_signal.emit(self.process_frame())


class VideoProcessor:

    def __init__(self):
        self.threshold = 80
        self.arc_coefficient = 0.035

    def find_shapes(self, contours):
        shapes = {
            'lines': 0,
            'triangles': 0,
            'rectangles': 0,
            'circles': 0
        }
        for contour in contours:
            arc_length = cv2.arcLength(contour, True)
            if arc_length > 100 and arc_length < 300:
                sides = cv2.approxPolyDP(
                    contour,
                    self.arc_coefficient*arc_length,
                    True
                )
                num_sides = len(sides)
                if num_sides == 2:
                    shapes['lines'] += 1
                elif num_sides == 3:
                    shapes['triangles'] += 1
                elif num_sides == 4:
                    shapes['rectangles'] += 1
                elif num_sides > 4:
                    shapes['circles'] += 1
        return shapes

    def make_binary(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(
            frame,
            self.threshold,
            255,
            cv2.THRESH_BINARY
        )
        frame, contours, h = cv2.findContours(
            frame,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(frame, contours, -1, (120, 120, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        return frame, contours

    def convert_to_qpixmap(self, frame):
        data = frame.data
        height, width, channel = frame.shape
        bytes_per_line = width * 3
        q_frame = QImage(
            data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGB888
        )
        q_frame = QPixmap.fromImage(q_frame)
        return q_frame
