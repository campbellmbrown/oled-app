from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtWidgets import QToolButton

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 64


class GalleryItem(QToolButton):
    def __init__(self, image_path: str, title: str) -> None:
        super().__init__()

        image = QImage(image_path).convertToFormat(QImage.Format.Format_Grayscale8)

        assert image.width() == IMAGE_WIDTH, f"Image width expected to be {IMAGE_WIDTH}px, got {image.width()}px"
        assert image.height() == IMAGE_HEIGHT, f"Image height expected to be {IMAGE_HEIGHT}px, got {image.height()}px"
        self.setIcon(QIcon(QPixmap.fromImage(image)))
        self.setText(title)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(IMAGE_WIDTH, IMAGE_HEIGHT))
        self.setAutoRaise(True)

        self.setStyleSheet("""
            QToolButton {
                border: 1px solid black;
                border-radius: 4px;
                padding: 4px;
            }
            QToolButton:hover {
                border: 2px solid #0078d7;  /* highlight on hover */
            }
        """)
