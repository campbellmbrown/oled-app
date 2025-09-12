import logging

import qdarktheme
from PySide6.QtWidgets import QApplication
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

from app.log.log_controller import LogController
from app.main.main_view import MainView


class MainController:
    def __init__(self, view: MainView) -> None:
        self.view = view

        log_controller = LogController(view.log_view)
        log_controller.add_to_logger()
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Application started.")

        view.dark_theme_action.triggered.connect(lambda: self._change_theme("dark"))
        view.light_theme_action.triggered.connect(lambda: self._change_theme("light"))
        view.light_theme_action.setChecked(True)
        self._change_theme("light")

        view.refresh_button.clicked.connect(self._populate_ports)
        self._populate_ports()

    def get_selected_port(self) -> str:
        selected_port = self.view.port_options.currentData()
        if selected_port is None:
            raise ValueError("No valid serial port selected.")
        assert isinstance(selected_port, ListPortInfo)
        return selected_port.device

    def _populate_ports(self) -> None:
        self.view.port_options.clear()
        ports = list_ports.comports()
        for port in ports:
            display = f"{port.device} - {port.description}"
            self.view.port_options.addItem(display, userData=port)

    def _change_theme(self, theme: str):
        """Change the application theme."""
        stylesheet = qdarktheme.load_stylesheet(theme)
        application = QApplication.instance()
        assert isinstance(application, QApplication)
        application.setStyleSheet(stylesheet)
