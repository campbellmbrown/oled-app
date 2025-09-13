import os

import yaml
from PySide6.QtCore import QObject, Signal

from app.animation.animation_frame import AnimationFrame
from app.animation.animation_item import AnimationItem
from app.animation.animation_view import AnimationView

ANIMATIONS_FILE = os.path.join("app", "animations.yml")


class AnimationController(QObject):
    signal_animation_selected = Signal(list, bool)

    def __init__(self, view: AnimationView) -> None:
        super().__init__()
        self.view = view

        with open(ANIMATIONS_FILE, encoding="utf-8") as file:
            animations = yaml.safe_load(file)

        for animation in animations:
            frames: list[AnimationFrame] = []
            for frame in animation["frames"]:
                frames.append(
                    AnimationFrame(
                        image_path=os.path.join(frame["image"]),
                        duration=frame["duration"],
                    )
                )
            is_random = animation.get("random", False)
            item = AnimationItem(animation["name"], frames, is_random)
            self.view.animation_layout.addWidget(item)

            item.clicked.connect(
                lambda _, frames=frames, is_random=is_random: self.signal_animation_selected.emit(frames, is_random)
            )
