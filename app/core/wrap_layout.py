from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtWidgets import QLayout, QLayoutItem, QSizePolicy, QWidget


class WrapLayout(QLayout):
    def __init__(self, parent: QWidget | None = None, margin: int = 0, hspacing: int = 0, vspacing: int = 0) -> None:
        super().__init__(parent)
        self.hspacing = hspacing
        self.vspacing = vspacing
        self.items: list[QLayoutItem] = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self) -> None:
        del self.items[:]

    def addItem(self, item: QLayoutItem) -> None:
        self.items.append(item)

    def horizontalSpacing(self) -> int:
        return self.hspacing

    def verticalSpacing(self) -> int:
        return self.vspacing

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int) -> QLayoutItem | None:
        if 0 <= index < len(self.items):
            return self.items[index]
        return None

    def takeAt(self, index: int) -> QLayoutItem:
        if 0 <= index < len(self.items):
            return self.items.pop(index)

    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self.doLayout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect: QRect) -> None:
        super().setGeometry(rect)
        self.doLayout(rect, test_only=False)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()
        for item in self.items:
            size = size.expandedTo(item.minimumSize())
        content_margins = self.getContentsMargins()
        assert isinstance(content_margins, tuple)
        left, top, right, bottom = content_margins
        size += QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect: QRect, test_only: bool) -> int:
        content_margins = self.getContentsMargins()
        assert isinstance(content_margins, tuple)
        left, top, right, bottom = content_margins
        assert isinstance(left, int)
        assert isinstance(top, int)
        assert isinstance(right, int)
        assert isinstance(bottom, int)
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        line_height = 0
        for item in self.items:
            widget = item.widget()
            h_space = self.horizontalSpacing()
            if h_space == -1:
                h_space = widget.style().layoutSpacing(
                    QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Horizontal
                )
            v_space = self.verticalSpacing()
            if v_space == -1:
                v_space = widget.style().layoutSpacing(
                    QSizePolicy.ControlType.PushButton, QSizePolicy.ControlType.PushButton, Qt.Orientation.Vertical
                )
            next_x = x + item.sizeHint().width() + h_space
            if next_x - h_space > effective.right() and line_height > 0:
                x = effective.x()
                y = y + line_height + v_space
                next_x = x + item.sizeHint().width() + h_space
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = next_x
            line_height = max(line_height, item.sizeHint().height())
        return y + line_height - rect.y() + bottom
