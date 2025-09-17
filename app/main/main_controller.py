import logging
import random

import qdarktheme  # type: ignore[import-untyped]
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from serial.tools import list_ports
from serial.tools.list_ports_common import ListPortInfo

from app.animation.animation_controller import AnimationController
from app.animation.animation_frame import AnimationFrame
from app.gallery.gallery_controller import GalleryController
from app.image_sender import send_image
from app.image_settings import ImageSettings
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

        self.gallery_controller = GalleryController(view.gallery_view)
        self.gallery_controller.signal_image_selected.connect(self._on_image_selected)

        self.animation_controller = AnimationController(view.animation_view)
        self.animation_controller.signal_animation_selected.connect(self._on_animation_selected)
        self.running_animation: list[AnimationFrame] | None = None
        self.animation_frame_index = 0
        self.is_animation_random = False
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_animation)

        view.invert_checkbox.setChecked(True)
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

    def _change_theme(self, theme: str) -> None:
        """Change the application theme."""
        stylesheet = qdarktheme.load_stylesheet(theme)
        application = QApplication.instance()
        assert isinstance(application, QApplication)
        application.setStyleSheet(stylesheet)

    def _on_image_selected(self, image_path: str) -> None:
        self.animation_timer.stop()
        self.running_animation = None
        send_image(image_path, self.get_selected_port(), self._get_image_settings())

    def _on_animation_selected(self, frames: list[AnimationFrame], is_random: bool) -> None:
        self.running_animation = frames
        self.animation_frame_index = 0
        self.is_animation_random = is_random
        self.animation_timer.start(int(frames[0].duration * 1000))

    def _update_animation(self) -> None:
        self.animation_timer.stop()
        if not self.running_animation:
            return

        if self.is_animation_random:
            if len(self.running_animation) > 1:
                choices = [i for i in range(len(self.running_animation)) if i != self.animation_frame_index]
                self.animation_frame_index = random.choice(choices)
        else:
            self.animation_frame_index += 1
            if self.animation_frame_index >= len(self.running_animation):
                self.animation_frame_index = 0

        frame = self.running_animation[self.animation_frame_index]
        send_image(frame.image_path, self.get_selected_port(), self._get_image_settings())

        self.animation_timer.start(int(frame.duration * 1000))

    def _get_image_settings(self) -> ImageSettings:
        return ImageSettings(
            invert=self.view.invert_checkbox.isChecked(),
            threshold=self.view.threshold.value(),
        )
