from dataclasses import dataclass


@dataclass(frozen=True)
class Detection:
    class_id: int
    label: str
    confidence: float
    xyxy: tuple  # Pixel box like (x1, y1, x2, y2)


@dataclass(frozen=True)
class AnalysisResult:
    width: int
    height: int
    detections: tuple
    inference_ms: float


class AnalysisError(Exception):
    pass
