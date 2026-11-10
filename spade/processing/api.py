from abc import ABC, abstractmethod
from time import perf_counter

from spade.acquisition.api import Frame

from .models import AnalysisError, AnalysisResult, Detection


class Detector(ABC):
    @abstractmethod
    def detect(self, frame: Frame) -> tuple:
        pass


def analyze(frame: Frame, detector: Detector) -> AnalysisResult:
    start = perf_counter()
    detections = detector.detect(frame)
    return AnalysisResult(
        width=frame.width,
        height=frame.height,
        detections=detections,
        inference_ms=(perf_counter() - start) * 1000,
    )
