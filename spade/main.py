import torch

from spade.acquisition.adapters import HttpSnapshotSource, VideoFileSource
from spade.config import parse_settings
from spade.monitoring.api import Monitor
from spade.moonraker import Moonraker
from spade.processing.adapters import RFDETRDetector, YoloDetector
from spade.ui.app import SPADEApp


def main(argv=None) -> None:
    settings = parse_settings(argv)

    device = settings.device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    printer = Moonraker(settings.printer_url)
    if settings.model == "yolo":
        detector = YoloDetector(
            settings.model_path, settings.confidence, settings.image_size, device
        )
    elif settings.model == "rfdetr":
        detector = RFDETRDetector(settings.model_path, settings.confidence, device)
    else:
        raise ValueError("model must be yolo or rfdetr")
    monitor = Monitor(
        live_source=HttpSnapshotSource(settings.camera_url),
        recorded_source=VideoFileSource(settings.video_path),
        detector=detector,
    )

    app = SPADEApp(printer, monitor)
    app.mainloop()


if __name__ == "__main__":
    main()
