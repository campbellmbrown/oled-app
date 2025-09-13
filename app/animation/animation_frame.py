from dataclasses import dataclass


@dataclass
class AnimationFrame:
    image_path: str
    duration: float
