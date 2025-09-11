import sys

from PySide6.QtWidgets import QApplication

from app.main.main_view import MainView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_view = MainView()
    main_view.show()

    sys.exit(app.exec())
