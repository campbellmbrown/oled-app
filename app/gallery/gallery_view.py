from app.core.page_base import PageBase
from app.core.wrap_layout import WrapLayout


class GalleryView(PageBase):
    def __init__(self) -> None:
        super().__init__()

        self.gallery_layout = WrapLayout(self, margin=20, hspacing=10, vspacing=10)
        self.set_layout(self.gallery_layout)
