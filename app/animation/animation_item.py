import random

from PySide6.QtCore import QEvent, QSize, Qt, QTimer
from PySide6.QtGui import QEnterEvent, QIcon, QImage, QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QToolButton

from app.animation.animation_frame import AnimationFrame

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 64


class AnimationItem(QToolButton):
    def __init__(self, name: str, frames: list[AnimationFrame], is_random: bool) -> None:
        super().__init__()
        self.frames = frames
        self.name = name
        self.is_random = is_random
        self.current_frame_index = 0

        # Preload QPixmaps for all frames
        self.pixmaps = []
        for frame in frames:
            print(frame.image_path)
            image = QImage(frame.image_path).convertToFormat(QImage.Format.Format_Grayscale8)
            assert image.width() == IMAGE_WIDTH, f"Image width expected {IMAGE_WIDTH}px, got {image.width()}px"
            assert image.height() == IMAGE_HEIGHT, f"Image height expected {IMAGE_HEIGHT}px, got {image.height()}px"
            self.pixmaps.append(QPixmap.fromImage(image))

        self.setIcon(QIcon(self.pixmaps[0]))
        self.setText(name)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(IMAGE_WIDTH, IMAGE_HEIGHT))
        self.setAutoRaise(True)

        # Remove border from stylesheet
        self.setStyleSheet("""
            QToolButton {
                border: none;
                padding: 4px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setXOffset(2)
        shadow.setYOffset(2)
        shadow.setColor(Qt.GlobalColor.black)
        self.setGraphicsEffect(shadow)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.current_frame_index = 0
        self.setIcon(QIcon(self.pixmaps[0]))
        if self.frames:
            self.timer.start(int(self.frames[0].duration * 1000))
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.timer.stop()
        self.setIcon(QIcon(self.pixmaps[0]))
        super().leaveEvent(event)

    def next_frame(self) -> None:
        if self.is_random:
            if len(self.frames) > 1:
                choices = [i for i in range(len(self.frames)) if i != self.current_frame_index]
                self.current_frame_index = random.choice(choices)
        else:
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.frames):
                self.current_frame_index = 0

        self.setIcon(QIcon(self.pixmaps[self.current_frame_index]))
        self.timer.start(int(self.frames[self.current_frame_index].duration * 1000))
