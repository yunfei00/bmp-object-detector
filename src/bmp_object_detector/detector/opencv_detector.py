from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True)
class BoundingBox:
    x: int
    y: int
    w: int
    h: int

    @property
    def area(self) -> int:
        return self.w * self.h


class OpenCVDetector:
    """Classic OpenCV-based detector for BMP objects."""

    def __init__(self, min_area: int = 200, blur_kernel: tuple[int, int] = (5, 5)) -> None:
        self.min_area = min_area
        self.blur_kernel = blur_kernel

    def detect(self, image: np.ndarray) -> list[BoundingBox]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, self.blur_kernel, 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes: list[BoundingBox] = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            boxes.append(BoundingBox(x=x, y=y, w=w, h=h))

        boxes.sort(key=lambda b: (b.y, b.x))
        return boxes
