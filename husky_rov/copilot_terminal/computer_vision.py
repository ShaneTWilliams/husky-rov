import cv2
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class VideoStream(QThread):

    frame_signal = pyqtSignal(QPixmap)
    binary_frame_signal = pyqtSignal(QPixmap)

    def __init__(self, ip):
        QThread.__init__(self)
        self.source = cv2.VideoCapture(ip)
        self.procesor = VideoProcessor(50)

    def grab_frame(self):
        img_valid, frame = self.source.read()
        if img_valid:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            data = rgb_frame.data
            height, width, channel = rgb_frame.shape
            bytes_per_line = width * 3
            q_frame = QImage(data, width, height, bytes_per_line, QImage.Format_RGB888)
            q_frame = QPixmap.fromImage(q_frame)
            return q_frame
        else:
            return None

    def run(self):
        while True:
            frame = self.grab_frame()
            if frame:
                self.frame_signal.emit(frame)


class VideoProcessor:

    def __init__(self, threshold):
        self.threshold = threshold

    def clean_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img = cv2.threshold(img, self.threshold, 255, cv2.THRESH_BINARY)
        img, contours, h = cv2.findContours(img,
                                            cv2.RETR_LIST,
                                            cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (120, 120, 0), 2)

        return img, contours

    def find_shapes(self, contours):
        lines = 0
        tris = 0
        rects = 0
        circles = 0
        for cnt in contours:
            arc = cv2.arcLength(cnt, True)
            if arc > 100 and arc < 300:
                approx_contour = cv2.approxPolyDP(cnt, 0.035*arc, True)
                sides = len(approx_contour)
                if sides == 2:
                    lines += 1
                elif sides == 3:
                    tris += 1
                elif sides == 4:
                    rects += 1
                elif sides > 4:
                    circles += 1
        return (lines, tris, rects, circles)
