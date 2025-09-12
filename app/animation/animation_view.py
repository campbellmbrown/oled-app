from PySide6.QtWidgets import QScrollArea, QWidget

from app.core.wrap_layout import WrapLayout


class AnimationView(QScrollArea):
    def __init__(self) -> None:
        super().__init__()
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)
        self.animation_layout = WrapLayout(self, margin=20, hspacing=10, vspacing=10)

        # Create a QWidget to hold the layout and to be contained in the QScrollArea
        widget = QWidget()
        widget.setLayout(self.animation_layout)
        self.setWidget(widget)
