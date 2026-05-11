from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


@dataclass(frozen=True)
class DetectorParams:
    min_area: int
    max_area: int | None
    threshold_mode: str
    threshold: int
    blur_size: int
    invert: bool
    show_index: bool


class ParamsPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        group = QGroupBox("参数")
        form = QFormLayout(group)

        self.min_area = QSpinBox(); self.min_area.setRange(1, 10_000_000); self.min_area.setValue(100)
        self.max_area = QLineEdit(); self.max_area.setPlaceholderText("可空")
        self.threshold_mode = QComboBox(); self.threshold_mode.addItems(["OTSU", "Adaptive", "Manual"])
        self.threshold = QSpinBox(); self.threshold.setRange(0, 255); self.threshold.setValue(128)
        self.blur_size = QSpinBox(); self.blur_size.setRange(1, 99); self.blur_size.setSingleStep(2); self.blur_size.setValue(5)
        self.invert = QCheckBox("invert")
        self.show_index = QCheckBox("show_index")

        form.addRow("min_area", self.min_area)
        form.addRow("max_area", self.max_area)
        form.addRow("threshold_mode", self.threshold_mode)
        form.addRow("threshold", self.threshold)
        form.addRow("blur_size", self.blur_size)
        form.addRow(self.invert)
        form.addRow(self.show_index)

        layout.addWidget(group)
        layout.addStretch(1)

    def values(self) -> DetectorParams:
        max_area_text = self.max_area.text().strip()
        max_area = int(max_area_text) if max_area_text else None
        mode_map = {"OTSU": "otsu", "Adaptive": "adaptive", "Manual": "manual"}
        return DetectorParams(
            min_area=self.min_area.value(),
            max_area=max_area,
            threshold_mode=mode_map[self.threshold_mode.currentText()],
            threshold=self.threshold.value(),
            blur_size=self.blur_size.value(),
            invert=self.invert.isChecked(),
            show_index=self.show_index.isChecked(),
        )
