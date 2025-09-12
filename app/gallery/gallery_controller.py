import logging
import os

from PySide6.QtCore import QObject, Signal

from app.gallery.gallery_item import GalleryItem
from app.gallery.gallery_view import GalleryView

IMAGE_DIR = os.path.join("app", "images")


class GalleryController(QObject):
    signal_image_selected = Signal(str)

    def __init__(self, view: GalleryView) -> None:
        super().__init__()
        self.view = view

        for filename in os.listdir(IMAGE_DIR):
            if filename.endswith(".png"):
                logging.info(f"Loading gallery item: {filename}")
                file_path = os.path.join(IMAGE_DIR, filename)
                item = GalleryItem(file_path, os.path.splitext(filename)[0])
                self.view.gallery_layout.addWidget(item)

                item.clicked.connect(lambda _, path=file_path: self.signal_image_selected.emit(path))
