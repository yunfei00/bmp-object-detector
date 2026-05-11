from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from bmp_object_detector.detector.opencv_detector import OpenCVDetector
from bmp_object_detector.io.image_io import load_bmp_image


def test_detect_rectangles_on_synthetic_bmp(tmp_path: Path) -> None:
    img = np.zeros((200, 300, 3), dtype=np.uint8)
    cv2.rectangle(img, (20, 30), (120, 150), (255, 255, 255), -1)
    cv2.rectangle(img, (170, 60), (260, 180), (255, 255, 255), -1)

    bmp_path = tmp_path / "test.bmp"
    assert cv2.imwrite(str(bmp_path), img)

    loaded = load_bmp_image(bmp_path)
    detector = OpenCVDetector(min_area=1000)
    results = detector.detect(loaded)

    assert len(results) == 2

    xs = sorted([r.bbox.x for r in results])
    assert xs[0] <= 25
    assert xs[1] >= 165


def test_detection_result_bbox_has_required_fields(tmp_path: Path) -> None:
    img = np.zeros((80, 80, 3), dtype=np.uint8)
    cv2.rectangle(img, (10, 10), (40, 50), (255, 255, 255), -1)
    bmp_path = tmp_path / "one.bmp"
    assert cv2.imwrite(str(bmp_path), img)

    loaded = load_bmp_image(bmp_path)
    results = OpenCVDetector(min_area=50).detect(loaded)

    assert len(results) == 1
    bbox = results[0].bbox
    for key in ("x", "y", "w", "h", "area"):
        assert hasattr(bbox, key)
