from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QToolButton

from app import oled


class GalleryItem(QToolButton):
    def __init__(self, image_path: str, title: str) -> None:
        super().__init__()
        self.image_path = image_path

        image = QImage(image_path).convertToFormat(QImage.Format.Format_Grayscale8)

        # Image must be either 128x64 or 64x128 (rotated)
        assert (image.width() == oled.WIDTH and image.height() == oled.HEIGHT) or (
            image.width() == oled.HEIGHT and image.height() == oled.WIDTH
        )

        self.setIcon(QIcon(QPixmap.fromImage(image)))
        self.setText(title)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(image.width(), image.height()))
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
