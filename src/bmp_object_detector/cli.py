from __future__ import annotations

from pathlib import Path

import typer

from bmp_object_detector.detector.opencv_detector import OpenCVDetector
from bmp_object_detector.gui.__main__ import run_gui
from bmp_object_detector.io.image_io import load_bmp_image, save_detection_json, save_image
from bmp_object_detector.visualization.draw import draw_boxes

app = typer.Typer(help="BMP object detector CLI")


@app.command()
def detect(
    input: Path = typer.Option(..., "--input", exists=True, file_okay=True, dir_okay=False),
    output: Path = typer.Option(Path("output"), "--output", file_okay=False, dir_okay=True),
    min_area: int = typer.Option(200, "--min-area", min=1, help="Minimum contour area to keep."),
) -> None:
    """Detect objects in a BMP image and save annotated image + JSON."""
    if input.suffix.lower() != ".bmp":
        raise typer.BadParameter("Only .bmp files are supported in phase 1.")

    image = load_bmp_image(input)
    detector = OpenCVDetector(min_area=min_area)
    results = detector.detect(image)

    annotated = draw_boxes(image, results)

    output.mkdir(parents=True, exist_ok=True)
    image_path = output / "result.png"
    json_path = output / "result.json"

    save_image(image_path, annotated)
    save_detection_json(json_path, input_path=input, image_shape=image.shape, results=results)

    typer.echo(f"Saved annotated image: {image_path}")
    typer.echo(f"Saved detection JSON: {json_path}")


@app.command()
def gui() -> None:
    """Launch the PySide6 desktop GUI."""
    run_gui()
