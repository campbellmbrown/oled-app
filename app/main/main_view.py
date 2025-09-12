from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.gallery.gallery_view import GalleryView


class MainView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 800)
        self._set_up_menu()
        self._set_up_port_selection()

        layout = QVBoxLayout()
        gallery_view = GalleryView()

        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Port:"))
        control_layout.addWidget(self.port_options)
        control_layout.addWidget(self.refresh_button)
        control_layout.addStretch()

        layout.addLayout(control_layout)
        layout.addWidget(gallery_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _set_up_menu(self) -> None:
        file_menu = QMenu("&File", self)
        file_menu.addAction("E&xit", self.close)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

    def _set_up_port_selection(self) -> None:
        self.port_options = QComboBox()
        self.port_options.setFixedWidth(300)
        self.refresh_button = QToolButton()
        refresh_button_style = self.refresh_button.style()
        assert isinstance(refresh_button_style, QStyle)
        icon = refresh_button_style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.refresh_button.setIcon(icon)
        self.refresh_button.setToolTip("Refresh")
