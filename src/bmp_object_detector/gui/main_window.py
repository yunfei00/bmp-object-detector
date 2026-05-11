from __future__ import annotations

from pathlib import Path

import cv2
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import QFileDialog, QHBoxLayout, QMainWindow, QMessageBox, QWidget

from bmp_object_detector.detector.opencv_detector import OpenCVDetector
from bmp_object_detector.gui.image_view import ImageView
from bmp_object_detector.gui.params_panel import ParamsPanel
from bmp_object_detector.gui.result_table import ResultTable
from bmp_object_detector.io.image_io import build_detection_payload, load_bmp_image, save_image
from bmp_object_detector.visualization.draw import draw_boxes


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BMP Object Detector")
        self.input_path: Path | None = None
        self.original_image = None
        self.annotated_image = None
        self.results = []
        self.selected_index: int | None = None

        toolbar = self.addToolBar("main")
        a_open = QAction("打开 BMP 图片", self); a_open.triggered.connect(self.open_image)
        a_detect = QAction("开始检测", self); a_detect.triggered.connect(self.run_detection)
        a_save_img = QAction("保存结果图片", self); a_save_img.triggered.connect(self.save_result_image)
        a_save_json = QAction("保存 JSON", self); a_save_json.triggered.connect(self.save_result_json)
        a_clear = QAction("清空结果", self); a_clear.triggered.connect(self.clear_results)
        for a in [a_open, a_detect, a_save_img, a_save_json, a_clear]: toolbar.addAction(a)

        center = QWidget(); layout = QHBoxLayout(center)
        self.params = ParamsPanel(); self.image_view = ImageView(); self.table = ResultTable()
        self.image_view.bbox_selected.connect(self._on_image_bbox_selected)
        self.table.row_selected.connect(self._on_table_row_selected)
        layout.addWidget(self.params, 1)
        layout.addWidget(self.image_view, 4)
        layout.addWidget(self.table, 2)
        self.setCentralWidget(center)

    def _to_pixmap(self, image) -> QPixmap:
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, c = rgb.shape
        qimg = QImage(rgb.data, w, h, c * w, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(qimg.copy())

    def open_image(self) -> None:
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "选择 BMP", "", "BMP Files (*.bmp)")
            if not file_name:
                return
            path = Path(file_name)
            self.original_image = load_bmp_image(path)
            self.input_path = path
            self.annotated_image = None
            self.results = []
            self.table.clear_results()
            self.selected_index = None
            self.image_view.set_detections([])
            self.image_view.clear_selection()
            self.image_view.set_pixmap(self._to_pixmap(self.original_image))
            self.image_view.reset_view()
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "错误", str(exc))

    def run_detection(self) -> None:
        try:
            if self.original_image is None:
                raise ValueError("请先打开 BMP 图片")
            p = self.params.values()
            detector = OpenCVDetector(
                min_area=p.min_area,
                max_area=p.max_area,
                blur_size=p.blur_size,
                threshold_mode=p.threshold_mode,
                threshold=p.threshold,
                invert=p.invert,
            )
            self.results = detector.detect(self.original_image)
            self.selected_index = None
            self.annotated_image = draw_boxes(self.original_image, self.results, show_index=p.show_index)
            self.table.set_results(self.results)
            self.table.clear_selection()
            self.image_view.set_pixmap(self._to_pixmap(self.original_image))
            self.image_view.set_detections(self.results)
            self.image_view.clear_selection()
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "错误", str(exc))

    def save_result_image(self) -> None:
        try:
            if self.annotated_image is None:
                raise ValueError("没有可保存的检测结果图片")
            file_name, _ = QFileDialog.getSaveFileName(self, "保存结果图片", "result.png", "PNG Files (*.png)")
            if not file_name:
                return
            save_image(Path(file_name), self.annotated_image)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "错误", str(exc))

    def save_result_json(self) -> None:
        try:
            if self.input_path is None or self.original_image is None:
                raise ValueError("没有可保存的检测结果")
            file_name, _ = QFileDialog.getSaveFileName(self, "保存 JSON", "result.json", "JSON Files (*.json)")
            if not file_name:
                return
            payload = build_detection_payload(self.input_path, self.original_image.shape, self.results)
            Path(file_name).write_text(__import__("json").dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "错误", str(exc))

    def clear_results(self) -> None:
        try:
            self.results = []
            self.annotated_image = None
            self.table.clear_results()
            self.selected_index = None
            self.image_view.set_detections([])
            self.image_view.clear_selection()
            if self.original_image is not None:
                self.image_view.set_pixmap(self._to_pixmap(self.original_image))
                self.image_view.reset_view()
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "错误", str(exc))

    def _on_image_bbox_selected(self, index: int | None) -> None:
        self.selected_index = index
        self.image_view.set_selected_index(index)
        self.table.blockSignals(True)
        if index is None:
            self.table.clear_selection()
        else:
            self.table.select_detection(index)
        self.table.blockSignals(False)

    def _on_table_row_selected(self, index: int | None) -> None:
        self.selected_index = index
        self.image_view.set_selected_index(index)
        if index is None:
            return
        detection = next((item for item in self.results if item.index == index), None)
        if detection is None:
            return
        box = detection.bbox
        self.image_view.centerOn(box.x + box.w / 2, box.y + box.h / 2)
