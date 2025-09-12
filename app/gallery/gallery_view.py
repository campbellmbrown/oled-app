from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QPushButton

from app.core.page_base import PageBase
from app.core.wrap_layout import WrapLayout

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 64


class GalleryView(PageBase):
    def __init__(self):
        super().__init__()

        layout = WrapLayout(self, margin=20, hspacing=10, vspacing=10)

        for _ in range(1, 50):
            button = QPushButton()
            pixmap = QPixmap("scripts/test.png")
            assert pixmap.width() == IMAGE_WIDTH
            assert pixmap.height() == IMAGE_HEIGHT
            button.setIcon(QIcon(pixmap))
            button.setIconSize(QSize(IMAGE_WIDTH, IMAGE_HEIGHT))
            button.setFixedSize(IMAGE_WIDTH + 10, IMAGE_HEIGHT + 10)
            layout.addWidget(button)

        self.set_layout(layout)
