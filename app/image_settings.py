from dataclasses import dataclass


@dataclass
class ImageSettings:
    invert: bool
    threshold: int
