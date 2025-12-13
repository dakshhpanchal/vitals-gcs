from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor

class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.aspect_w = 2
        self.aspect_h = 1
        self.setMinimumSize(320, 160)

    def sizeHint(self):
        return QSize(960, 480)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        return int(w * self.aspect_h / self.aspect_w)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setBrush(QColor(42,42,42))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(self.rect(), 16, 16)

        p.setPen(Qt.white)
        p.drawText(self.rect(), Qt.AlignCenter, "Video Feed (2:1)")
