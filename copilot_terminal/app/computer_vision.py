import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class VideoProcessor(QThread):

    video_signal = pyqtSignal(QPixmap)
    shape_signal = pyqtSignal(dict)

    def __init__(self):
        QThread.__init__(self)
        self.source = cv2.VideoCapture('http://192.168.2.99:8081')
        self.threshold = 80
        self.arc_coefficient = 0.035
        self.show_binary_video = False
        self.is_running = False

    def run(self):
        self.is_running = True
        while True:
            if self.is_running:
                raw_frame = self.grab_frame()
                binary_frame, contours = self.make_binary(raw_frame)
                shape_count = self.find_shapes(contours)
                self.shape_signal.emit(shape_count)
                if self.show_binary_video:
                    frame = self.convert_to_qpixmap(binary_frame)
                else:
                    frame = self.convert_to_qpixmap(raw_frame)
                self.video_signal.emit(frame)

    def grab_frame(self):
        img_valid, frame = self.source.read()
        if img_valid:
            return frame

    def make_binary(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, frame = cv2.threshold(
            frame,
            self.threshold,
            255,
            cv2.THRESH_BINARY
        )
        contours, h = cv2.findContours(
            frame,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE
        )
        cv2.drawContours(frame, contours, -1, (120, 120, 0), 2)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        return frame, contours

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

    def find_shapes(self, contours):
        shapes = {
            'lines': 0,
            'triangles': 0,
            'squares': 0,
            'circles': 0
        }
        for contour in contours:
            arc_length = cv2.arcLength(contour, True)
            if arc_length > 100 and arc_length < 500:
                sides = cv2.approxPolyDP(
                    contour,
                    self.arc_coefficient*arc_length,
                    True
                )
                num_sides = len(sides)
                bounding_rect = cv2.minAreaRect(contour)
                width = bounding_rect[1][0]
                height = bounding_rect[1][1]
                if height > width:
                    side_ratio = height / width
                else:
                    side_ratio = width / height
                if (side_ratio > 4 and side_ratio < 10) or num_sides == 2:
                    shapes['lines'] += 1
                    continue
                elif num_sides == 3:
                    shapes['triangles'] += 1
                elif num_sides == 4:
                    shapes['squares'] += 1
                elif num_sides > 4:
                    shapes['circles'] += 1
        return shapes
