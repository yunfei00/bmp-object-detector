from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import cv2
import numpy as np

ThresholdMode = Literal["otsu", "adaptive", "manual"]


@dataclass(frozen=True)
class BoundingBox:
    x: int
    y: int
    w: int
    h: int

    @property
    def area(self) -> int:
        return self.w * self.h


@dataclass(frozen=True)
class DetectionResult:
    index: int
    bbox: BoundingBox
    confidence: float = 1.0


class OpenCVDetector:
    """Classic OpenCV-based detector for BMP objects."""

    def __init__(
        self,
        min_area: int = 200,
        max_area: int | None = None,
        blur_size: int = 5,
        threshold_mode: ThresholdMode = "otsu",
        threshold: int = 128,
        invert: bool = False,
    ) -> None:
        self.min_area = min_area
        self.max_area = max_area
        self.blur_size = blur_size if blur_size % 2 == 1 else blur_size + 1
        self.threshold_mode = threshold_mode
        self.threshold = threshold
        self.invert = invert

    def _threshold_image(self, blurred: np.ndarray) -> np.ndarray:
        if self.threshold_mode == "adaptive":
            th_mode = cv2.THRESH_BINARY_INV if self.invert else cv2.THRESH_BINARY
            return cv2.adaptiveThreshold(
                blurred,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                th_mode,
                11,
                2,
            )

        flag = cv2.THRESH_BINARY_INV if self.invert else cv2.THRESH_BINARY
        if self.threshold_mode == "otsu":
            _, thresh = cv2.threshold(blurred, 0, 255, flag + cv2.THRESH_OTSU)
            return thresh

        _, thresh = cv2.threshold(blurred, self.threshold, 255, flag)
        return thresh

    def detect(self, image: np.ndarray) -> list[DetectionResult]:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (self.blur_size, self.blur_size), 0)
        thresh = self._threshold_image(blurred)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        results: list[DetectionResult] = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area:
                continue
            if self.max_area is not None and area > self.max_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            results.append(DetectionResult(index=0, bbox=BoundingBox(x=x, y=y, w=w, h=h), confidence=1.0))

        results.sort(key=lambda item: (item.bbox.y, item.bbox.x))
        return [DetectionResult(index=i + 1, bbox=item.bbox, confidence=item.confidence) for i, item in enumerate(results)]
