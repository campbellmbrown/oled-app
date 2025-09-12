import os

from app.gallery.gallery_item import GalleryItem
from app.gallery.gallery_view import GalleryView

IMAGE_DIR = "app/images"


class GalleryController:
    def __init__(self, view: GalleryView) -> None:
        self.view = view

        for filename in os.listdir(IMAGE_DIR):
            if filename.endswith(".png"):
                print(f"Loading gallery item: {filename}")
                file_path = os.path.join(IMAGE_DIR, filename)
                item = GalleryItem(file_path, os.path.splitext(filename)[0])
                self.view.gallery_layout.addWidget(item)
