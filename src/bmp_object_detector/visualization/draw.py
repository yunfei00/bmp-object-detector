from __future__ import annotations

import cv2
import numpy as np

from bmp_object_detector.detector.opencv_detector import BoundingBox


def draw_boxes(image: np.ndarray, boxes: list[BoundingBox]) -> np.ndarray:
    canvas = image.copy()
    for box in boxes:
        cv2.rectangle(canvas, (box.x, box.y), (box.x + box.w, box.y + box.h), (0, 255, 0), 2)
    return canvas
