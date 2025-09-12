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
            # If it's in the root image directory, add to "Misc" tab
            if path.endswith(".png"):
                file_path = os.path.join(IMAGE_DIR, path)
                self._add_item("Misc", file_path)

            # Else if is a directory, add to the tab named after the directory
            elif os.path.isdir(os.path.join(IMAGE_DIR, path)):
                tab_name = path.replace("_", " ").title()
                tab_path = os.path.join(IMAGE_DIR, path)
                for subpath in os.listdir(tab_path):
                    if subpath.endswith(".png"):
                        file_path = os.path.join(tab_path, subpath)
                        self._add_item(tab_name, file_path)

        self.view.random_button.clicked.connect(self._select_random_image)

    def _add_item(self, tab_name: str, file_path: str) -> None:
        logging.info(f"Loading item: {file_path}")
        self.view.add_to_tab(tab_name, self._create_item(file_path))
        self.view.add_to_tab("All", self._create_item(file_path))

    def _create_item(self, file_path: str) -> GalleryItem:
        name = os.path.splitext(os.path.basename(file_path))[0]
        item = GalleryItem(file_path, name)
        item.clicked.connect(lambda _, path=file_path: self.signal_image_selected.emit(path))
        return item

    def _select_random_image(self) -> None:
        item = random.choice(self.view.items)
        self.signal_image_selected.emit(item.image_path)
