import logging

from app.log.log_view import LogView


class LogController(logging.Handler):
    def __init__(self, view: LogView) -> None:
        super().__init__()
        self.view = view
        self.view.clear_button.clicked.connect(self._clear_logs)

    def add_to_logger(self) -> None:
        self.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logging.getLogger().addHandler(self)

    def emit(self, record: logging.LogRecord) -> None:
        log_entry = self.format(record)
        self.view.log_text.appendPlainText(log_entry)

    def _clear_logs(self) -> None:
        self.view.log_text.clear()
