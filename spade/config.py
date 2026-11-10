import argparse
from dataclasses import dataclass
from pathlib import Path
import tomllib


DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "spade.toml"
CONFIG_KEYS = (
    "printer_url", "camera_url", "video_path", "model_path", "confidence", "image_size",
)
PATH_KEYS = ("video_path", "model_path")


@dataclass(frozen=True)
class Settings:
    printer_url: str
    camera_url: str
    video_path: Path
    model_path: Path
    confidence: float
    image_size: int


def _read_config(path: Path) -> dict:
    with path.open("rb") as stream:
        values = tomllib.load(stream)
    for key in PATH_KEYS:
        if key in values:
            file_path = Path(values[key]).expanduser()
            values[key] = (path.parent / file_path).resolve()
    return values


def parse_settings(argv=None) -> Settings:
    parser = argparse.ArgumentParser(description="Run the SPADE demo", allow_abbrev=False)
    parser.add_argument("--config", type=Path, help="TOML file overriding the bundled spade.toml")
    parser.add_argument("--printer-url", help="Moonraker base URL")
    parser.add_argument("--camera-url", help="Live camera snapshot URL")
    parser.add_argument("--video", dest="video_path", type=Path, help="Recorded video file")
    parser.add_argument("--weights", dest="model_path", type=Path, help="YOLO checkpoint file")
    parser.add_argument("--confidence", type=float, help="YOLO detection threshold (0 to 1)")
    parser.add_argument("--image-size", type=int, help="YOLO inference image size")
    args = parser.parse_args(argv)

    values = _read_config(DEFAULT_CONFIG)
    if args.config is not None:
        values.update(_read_config(args.config.expanduser().resolve()))
    if args.printer_url is not None:
        values["printer_url"] = args.printer_url
    if args.camera_url is not None:
        values["camera_url"] = args.camera_url
    if args.video_path is not None:
        values["video_path"] = args.video_path.expanduser().resolve()
    if args.model_path is not None:
        values["model_path"] = args.model_path.expanduser().resolve()
    if args.confidence is not None:
        values["confidence"] = args.confidence
    if args.image_size is not None:
        values["image_size"] = args.image_size

    for key in CONFIG_KEYS:
        if key not in values:
            raise ValueError(f"Missing setting: {key}")
    return Settings(
        printer_url=values["printer_url"],
        camera_url=values["camera_url"],
        video_path=values["video_path"],
        model_path=values["model_path"],
        confidence=values["confidence"],
        image_size=values["image_size"],
    )
