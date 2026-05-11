from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from bmp_object_detector.detector.opencv_detector import DetectionResult


class ResultTable(QTableWidget):
    row_selected = Signal(object)
    HEADERS = ["index", "x", "y", "w", "h", "area", "confidence"]

    def __init__(self) -> None:
        super().__init__(0, len(self.HEADERS))
        self.setHorizontalHeaderLabels(self.HEADERS)
        self._row_to_index: dict[int, int] = {}
        self.itemSelectionChanged.connect(self._emit_selection)

    def set_results(self, results: list[DetectionResult]) -> None:
        self.setRowCount(len(results))
        self._row_to_index = {}
        for row, result in enumerate(results):
            self._row_to_index[row] = result.index
            box = result.bbox
            values = [result.index, box.x, box.y, box.w, box.h, box.area, f"{result.confidence:.1f}"]
            for col, value in enumerate(values):
                self.setItem(row, col, QTableWidgetItem(str(value)))

    def clear_results(self) -> None:
        self._row_to_index = {}
        self.setRowCount(0)

    def select_detection(self, index: int) -> None:
        row = self._row_for_index(index)
        if row is None:
            return
        self.selectRow(row)
        self.scrollToItem(self.item(row, 0))

    def clear_selection(self) -> None:
        self.clearSelection()

    def _row_for_index(self, index: int) -> int | None:
        for row, row_index in self._row_to_index.items():
            if row_index == index:
                return row
        return None

    def _emit_selection(self) -> None:
        rows = self.selectionModel().selectedRows()
        if not rows:
            self.row_selected.emit(None)
            return
        row = rows[0].row()
        self.row_selected.emit(self._row_to_index.get(row))
