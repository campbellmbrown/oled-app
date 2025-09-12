from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QToolButton

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 64


class GalleryItem(QToolButton):
    def __init__(self, image_path: str, title: str) -> None:
        super().__init__()
        pixmap = QPixmap(image_path)
        assert pixmap.width() == IMAGE_WIDTH, f"Image width expected to be {IMAGE_WIDTH}px, got {pixmap.width()}px"
        assert pixmap.height() == IMAGE_HEIGHT, f"Image height expected to be {IMAGE_HEIGHT}px, got {pixmap.height()}px"
        self.setIcon(QIcon(pixmap))
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
