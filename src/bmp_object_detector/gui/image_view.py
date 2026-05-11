from __future__ import annotations

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QPainter, QPen, QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene, QGraphicsView

from bmp_object_detector.detector.opencv_detector import DetectionResult


def find_hit_detection_index(point: QPointF, detections: list[DetectionResult]) -> int | None:
    """Return detection index that contains point; in overlap choose smallest area."""
    hits: list[DetectionResult] = []
    for detection in detections:
        box = detection.bbox
        if box.x <= point.x() <= box.x + box.w and box.y <= point.y() <= box.y + box.h:
            hits.append(detection)
    if not hits:
        return None
    return min(hits, key=lambda item: item.bbox.area).index


class ImageView(QGraphicsView):
    bbox_selected = Signal(object)

    def __init__(self) -> None:
        super().__init__()
        self._scene = QGraphicsScene(self)
        self._item = QGraphicsPixmapItem()
        self._scene.addItem(self._item)
        self.setScene(self._scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self._detections: list[DetectionResult] = []
        self._selected_index: int | None = None

    def set_pixmap(self, pixmap: QPixmap) -> None:
        self._item.setPixmap(pixmap)
        self.setSceneRect(self._item.boundingRect())

    def set_detections(self, detections: list[DetectionResult]) -> None:
        self._detections = detections
        self.viewport().update()

    def set_selected_index(self, index: int | None) -> None:
        self._selected_index = index
        self.viewport().update()

    def clear_selection(self) -> None:
        self.set_selected_index(None)

    def wheelEvent(self, event) -> None:  # type: ignore[override]
        factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
        self.scale(factor, factor)

    def reset_view(self) -> None:
        self.resetTransform()

    def mousePressEvent(self, event) -> None:  # type: ignore[override]
        if event.button() == Qt.LeftButton and self._detections:
            scene_point = self.mapToScene(event.position().toPoint())
            image_point = self._item.mapFromScene(scene_point)
            selected_index = find_hit_detection_index(image_point, self._detections)
            self.bbox_selected.emit(selected_index)
        super().mousePressEvent(event)

    def drawForeground(self, painter: QPainter, rect) -> None:  # type: ignore[override]
        super().drawForeground(painter, rect)
        if not self._detections:
            return
        normal_pen = QPen(Qt.green, 1)
        selected_pen = QPen(Qt.red, 3)
        for detection in self._detections:
            box = detection.bbox
            pen = selected_pen if detection.index == self._selected_index else normal_pen
            painter.setPen(pen)
            painter.drawRect(box.x, box.y, box.w, box.h)
            if detection.index == self._selected_index:
                painter.drawText(box.x + 4, box.y + 18, f"#{detection.index}")
