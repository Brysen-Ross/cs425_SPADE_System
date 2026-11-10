from spade.acquisition.api import FrameSource
from spade.processing.api import AnalysisError, Detector, analyze

from .models import Preview


class Monitor:

    def __init__(self, live_source: FrameSource, recorded_source: FrameSource, detector: Detector):
        self._live_source = live_source
        self._recorded_source = recorded_source
        self._source = live_source
        self._detector = detector
        self._preview = Preview()
        self._frame_number = 0
        self._cooldown_until_frame = 0
        self.paused = False

    @property
    def connected(self) -> bool:
        return self._source.connected

    @property
    def analysis_enabled(self) -> bool:
        return self._source is self._recorded_source

    def connect(self) -> bool:
        return self._source.connect()

    def select_live_camera(self) -> None:
        self._select_source(self._live_source)

    def select_recorded_video(self) -> None:
        self._select_source(self._recorded_source)

    def _select_source(self, source: FrameSource) -> None:
        if source is not self._source:
            self.disconnect()
            self._source = source
        if not self.connected:
            self.connect()

    def read_preview(self) -> Preview:
        if self.paused:
            return self._preview
        frame = self._source.read()
        if frame is None:
            self._preview = Preview()
            return self._preview

        self._frame_number += 1
        if not self.analysis_enabled:
            self._preview = Preview(frame)
            return self._preview

        try:
            analysis = analyze(frame, self._detector)
        except AnalysisError as error:
            print("SPADE: Analysis unavailable:", error)
            self._preview = Preview(frame=frame, error="Analysis unavailable")
            return self._preview

        self._preview = Preview(frame, analysis)
        if analysis.detections:
            confidence = max(d.confidence for d in analysis.detections)
            video_time = self._frame_number / self._source.fps
            print(
                f"Detection at {video_time:.2f}s | Confidence: {confidence:.1%} | "
                f"Inference: {analysis.inference_ms:.1f} ms"
            )
            if self._frame_number >= self._cooldown_until_frame:
                self.paused = True
                print("SPADE: Failure detected - video paused.")
        return self._preview

    def resume(self) -> None:
        if self.paused:
            self.paused = False
            self._cooldown_until_frame = self._frame_number + round(self._source.fps)
            print("SPADE: Video resumed.")

    def disconnect(self) -> None:
        self._source.disconnect()
        self._preview = Preview()
        self._frame_number = 0
        self._cooldown_until_frame = 0
        self.paused = False
