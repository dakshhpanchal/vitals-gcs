import pygame
from PySide6.QtCore import QObject, Signal, QTimer

class ControllerReader(QObject):
    updated = Signal(float, float, float, float)

    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.joystick.init()
        self.js = pygame.joystick.Joystick(0) if pygame.joystick.get_count() else None
        if self.js:
            self.js.init()

        self.timer = QTimer()
        self.timer.timeout.connect(self.read)
        self.timer.start(20)

    def read(self):
        if not self.js:
            return
        pygame.event.pump()
        self.updated.emit(
            self.js.get_axis(0),
            -self.js.get_axis(1),
            self.js.get_axis(3),
            -self.js.get_axis(4),
        )
