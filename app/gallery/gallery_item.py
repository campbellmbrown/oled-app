from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QToolButton

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 64


class GalleryItem(QToolButton):
    def __init__(self, image_path: str, title: str) -> None:
        super().__init__()
        self.image_path = image_path

        image = QImage(image_path).convertToFormat(QImage.Format.Format_Grayscale8)

        assert image.width() == IMAGE_WIDTH, f"Image width expected to be {IMAGE_WIDTH}px, got {image.width()}px"
        assert image.height() == IMAGE_HEIGHT, f"Image height expected to be {IMAGE_HEIGHT}px, got {image.height()}px"
        self.setIcon(QIcon(QPixmap.fromImage(image)))
        self.setText(title)
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
