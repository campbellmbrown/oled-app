from PySide6.QtWidgets import QMainWindow, QMenu, QMenuBar, QVBoxLayout, QWidget

from app.gallery.gallery_view import GalleryView


class MainView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 800)
        self._set_up_menu()

        layout = QVBoxLayout()
        gallery_view = GalleryView()

        layout.addWidget(gallery_view)
        cental_widget = QWidget()
        cental_widget.setLayout(layout)
        self.setCentralWidget(cental_widget)

    def _set_up_menu(self) -> None:
        file_menu = QMenu("&File", self)
        file_menu.addAction("E&xit", self.close)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)
