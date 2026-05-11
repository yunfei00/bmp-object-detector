from PySide6.QtCore import QPointF

from bmp_object_detector.detector.opencv_detector import BoundingBox, DetectionResult
from bmp_object_detector.gui.image_view import find_hit_detection_index


def test_hit_returns_correct_index() -> None:
    detections = [
        DetectionResult(index=1, bbox=BoundingBox(x=10, y=10, w=20, h=20)),
        DetectionResult(index=2, bbox=BoundingBox(x=50, y=50, w=10, h=10)),
    ]
    assert find_hit_detection_index(QPointF(15, 15), detections) == 1
    assert find_hit_detection_index(QPointF(55, 55), detections) == 2


def test_overlap_returns_smallest_area() -> None:
    detections = [
        DetectionResult(index=1, bbox=BoundingBox(x=10, y=10, w=100, h=100)),
        DetectionResult(index=2, bbox=BoundingBox(x=20, y=20, w=10, h=10)),
    ]
    assert find_hit_detection_index(QPointF(25, 25), detections) == 2


def test_blank_returns_none() -> None:
    detections = [DetectionResult(index=1, bbox=BoundingBox(x=10, y=10, w=20, h=20))]
    assert find_hit_detection_index(QPointF(200, 200), detections) is None
