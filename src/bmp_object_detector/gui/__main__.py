from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from bmp_object_detector.gui.main_window import MainWindow


def run_gui() -> None:
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(1400, 900)
    win.show()
    sys.exit(app.exec())
