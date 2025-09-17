from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDockWidget,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QSpinBox,
    QStyle,
    QTabWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.animation.animation_view import AnimationView
from app.gallery.gallery_view import GalleryView
from app.log.log_view import LogView


class MainView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(1000, 800)
        self._set_up_menu()
        self._set_up_dock()
        self._set_up_controls()

        layout = QVBoxLayout()
        self.gallery_view = GalleryView()
        self.animation_view = AnimationView()

        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Port:"))
        control_layout.addWidget(self.port_options)
        control_layout.addWidget(self.refresh_button)
        control_layout.addStretch()
        control_layout.addWidget(QLabel("Brightness:"))
        control_layout.addWidget(self.brightness)
        control_layout.addWidget(QLabel("Contrast:"))
        control_layout.addWidget(self.contrast)
        control_layout.addWidget(self.invert_checkbox)

        image_settings_layout = QHBoxLayout()
        image_settings_layout.addWidget(self.invert_checkbox)
        image_settings_layout.addStretch()

        tabs = QTabWidget()
        tabs.addTab(self.gallery_view, "Gallery")
        tabs.addTab(self.animation_view, "Animation")

        layout.addLayout(control_layout)
        layout.addWidget(tabs)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _set_up_menu(self) -> None:
        file_menu = QMenu("&File", self)
        preferences_menu = QMenu("&Preferences", self)
        theme_menu = QMenu("&Theme", self)

        self.light_theme_action = QAction("Light")
        self.dark_theme_action = QAction("Dark")

        theme_action_group = QActionGroup(self)
        theme_action_group.setExclusive(True)
        self.light_theme_action.setCheckable(True)
        self.dark_theme_action.setCheckable(True)
        theme_action_group.addAction(self.light_theme_action)
        theme_action_group.addAction(self.dark_theme_action)
        theme_menu.addAction(self.light_theme_action)
        theme_menu.addAction(self.dark_theme_action)

        file_menu.addMenu(preferences_menu)
        preferences_menu.addMenu(theme_menu)
        file_menu.addSeparator()
        file_menu.addAction("E&xit", self.close)

        menu_bar = QMenuBar()
        menu_bar.addMenu(file_menu)
        self.setMenuBar(menu_bar)

    def _set_up_dock(self) -> None:
        self.log_view = LogView()
        dock = QDockWidget("Log")
        dock.setWidget(self.log_view)
        dock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

    def _set_up_controls(self) -> None:
        self.port_options = QComboBox()
        self.port_options.setFixedWidth(300)

        self.refresh_button = QToolButton()
        refresh_button_style = self.refresh_button.style()
        assert isinstance(refresh_button_style, QStyle)
        icon = refresh_button_style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload)
        self.refresh_button.setIcon(icon)
        self.refresh_button.setToolTip("Refresh")

        self.invert_checkbox = QCheckBox("Invert Colors")
        self.invert_checkbox.setChecked(False)

        self.brightness = QSpinBox()
        self.brightness.setRange(-100, 100)
        self.brightness.setValue(0)
        self.brightness.setFixedWidth(80)

        self.contrast = QDoubleSpinBox()
        self.contrast.setRange(-1.0, 1.0)
        self.contrast.setValue(0.0)
        self.contrast.setSingleStep(0.1)
        self.contrast.setFixedWidth(80)
