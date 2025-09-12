from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QScrollArea, QTabWidget, QVBoxLayout, QWidget

from app.core.page_base import PageBase
from app.core.wrap_layout import WrapLayout
from app.gallery.gallery_item import GalleryItem


class GalleryTab(QScrollArea):
    def __init__(self) -> None:
        super().__init__()
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

        self.gallery_layout = WrapLayout(self, margin=20, hspacing=10, vspacing=10)

        # Create a QWidget to hold the layout and to be contained in the QScrollArea
        widget = QWidget()
        widget.setLayout(self.gallery_layout)
        self.setWidget(widget)


class GalleryView(PageBase):
    def __init__(self) -> None:
        super().__init__()
        self.items: list[GalleryItem] = []
        self.random_button = QPushButton("Random")

        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(True)

        self.tabs: dict[str, GalleryTab] = {}

        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.addWidget(self.random_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout)

    def add_to_tab(self, tab_name: str, item: GalleryItem) -> None:
        if tab_name not in self.tabs:
            new_tab = GalleryTab()
            self.tabs[tab_name] = new_tab
            self.tab_widget.addTab(new_tab, tab_name)

        self.tabs[tab_name].gallery_layout.addWidget(item)
        self.tabs[tab_name].gallery_layout.update()
        self.items.append(item)
