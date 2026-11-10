from spade.config import parse_settings

from spade.acquisition.adapters import HttpSnapshotSource, VideoFileSource
from spade.monitoring.api import Monitor
from spade.moonraker import Moonraker
from spade.processing.adapters import YoloDetector
from spade.ui.app import SPADEApp


def main(argv=None) -> None:
    settings = parse_settings(argv)

    printer = Moonraker(settings.printer_url)
    detector = YoloDetector(
        settings.model_path, confidence=settings.confidence, image_size=settings.image_size
    )
    monitor = Monitor(
        live_source=HttpSnapshotSource(settings.camera_url),
        recorded_source=VideoFileSource(settings.video_path),
        detector=detector,
    )

    app = SPADEApp(printer, monitor)
    app.mainloop()


if __name__ == "__main__":
    main()
