from PySide6.QtWidgets import QLayout, QScrollArea, QWidget


class PageBase(QScrollArea):
    def __init__(self) -> None:
        super().__init__()
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)

    def set_layout(self, layout: QLayout) -> None:
        # Create a QWidget to hold the layout and to be contained in the QScrollArea
        widget = QWidget()
        widget.setLayout(layout)
        self.setWidget(widget)
