from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

from bmp_object_detector.detector.opencv_detector import DetectionResult


def load_bmp_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Failed to read image: {path}")
    return image


def save_image(path: Path, image: np.ndarray) -> None:
    ok = cv2.imwrite(str(path), image)
    if not ok:
        raise ValueError(f"Failed to write image: {path}")


def build_detection_payload(input_path: Path, image_shape: tuple[int, ...], results: list[DetectionResult]) -> dict:
    height, width = image_shape[:2]
    return {
        "input": str(input_path),
        "image_width": int(width),
        "image_height": int(height),
        "count": len(results),
        "boxes": [
            {
                "x": r.bbox.x,
                "y": r.bbox.y,
                "w": r.bbox.w,
                "h": r.bbox.h,
                "area": r.bbox.area,
            }
            for r in results
        ],
    }


def save_detection_json(path: Path, input_path: Path, image_shape: tuple[int, ...], results: list[DetectionResult]) -> None:
    payload = build_detection_payload(input_path=input_path, image_shape=image_shape, results=results)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
