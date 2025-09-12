import logging
import os
import random

from PySide6.QtCore import QObject, Signal

from app.gallery.gallery_item import GalleryItem
from app.gallery.gallery_view import GalleryView

IMAGE_DIR = os.path.join("app", "images")


class GalleryController(QObject):
    signal_image_selected = Signal(str)

    def __init__(self, view: GalleryView) -> None:
        super().__init__()
        self.view = view

        for path in os.listdir(IMAGE_DIR):
            if path.endswith(".png"):
                file_path = os.path.join(IMAGE_DIR, path)
                logging.info(f"Loading item: {file_path}")
                name = os.path.splitext(path)[0]
                item = GalleryItem(file_path, name)
                self.view.add_to_tab("Misc", item)

                item.clicked.connect(lambda _, path=file_path: self.signal_image_selected.emit(path))

            # Else if is a directory, create a new tab and add its images
            elif os.path.isdir(os.path.join(IMAGE_DIR, path)):
                tab_name = path.replace("_", " ").title()
                tab_path = os.path.join(IMAGE_DIR, path)
                for subpath in os.listdir(tab_path):
                    if subpath.endswith(".png"):
                        file_path = os.path.join(tab_path, subpath)
                        logging.info(f"Loading item: {file_path}")
                        name = os.path.splitext(subpath)[0]
                        item = GalleryItem(file_path, name)
                        self.view.add_to_tab(tab_name, item)

                        item.clicked.connect(lambda _, path=file_path: self.signal_image_selected.emit(path))

        self.view.random_button.clicked.connect(self._select_random_image)

    def _select_random_image(self) -> None:
        item = random.choice(self.view.items)
        self.signal_image_selected.emit(item.image_path)
