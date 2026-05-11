from __future__ import annotations

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from bmp_object_detector.detector.opencv_detector import DetectionResult


class ResultTable(QTableWidget):
    HEADERS = ["index", "x", "y", "w", "h", "area", "confidence"]

    def __init__(self) -> None:
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)

    def set_results(self, results: list[DetectionResult]) -> None:
        self.setRowCount(len(results))
        for row, result in enumerate(results):
            box = result.bbox
            values = [result.index, box.x, box.y, box.w, box.h, box.area, f"{result.confidence:.1f}"]
            for col, value in enumerate(values):
                self.setItem(row, col, QTableWidgetItem(str(value)))

    def clear_results(self) -> None:
        self.setRowCount(0)
