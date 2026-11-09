from pathlib import Path

from spade.acquisition.api import Frame

from .models import AnalysisError, Detection


class YoloDetector:
    def __init__(self, model_path: Path, confidence: float, image_size: int):
        from ultralytics import YOLO

        self._model = YOLO(str(model_path))
        self._confidence = confidence
        self._image_size = image_size

    def detect(self, frame: Frame) -> tuple:
        try:
            result = self._model.predict(
                source=frame.image,
                imgsz=self._image_size,
                conf=self._confidence,
                verbose=False,
            )[0]
            boxes = result.boxes
            if boxes is None:
                return ()
            detections = []
            for box in boxes:
                class_id = int(box.cls[0])
                detection = Detection(
                    class_id=class_id,
                    label=result.names[class_id],
                    confidence=float(box.conf[0]),
                    xyxy=tuple(box.xyxy[0].tolist()),
                )
                detections.append(detection)
            return tuple(detections)
        except (RuntimeError, ValueError, OSError) as error:
            raise AnalysisError("Local YOLO inference failed") from error
