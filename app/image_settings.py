from dataclasses import dataclass


@dataclass
class ImageSettings:
    invert: bool
    brightness: int = 0
    contrast: float = 0
