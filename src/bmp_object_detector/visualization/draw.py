from __future__ import annotations

import cv2
import numpy as np

from bmp_object_detector.detector.opencv_detector import DetectionResult


def draw_boxes(image: np.ndarray, results: list[DetectionResult], show_index: bool = False) -> np.ndarray:
    canvas = image.copy()
    for result in results:
        box = result.bbox
        cv2.rectangle(canvas, (box.x, box.y), (box.x + box.w, box.y + box.h), (0, 255, 0), 2)
        if show_index:
            cv2.putText(
                canvas,
                str(result.index),
                (box.x, max(12, box.y - 6)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )
    return canvas
