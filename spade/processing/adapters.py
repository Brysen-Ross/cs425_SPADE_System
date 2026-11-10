from pathlib import Path

import cv2
from PIL import Image
from rfdetr import RFDETR
from ultralytics import YOLO

from spade.acquisition.api import Frame

from .models import AnalysisError, Detection


class YoloDetector:
    def __init__(self, model_path: Path, confidence: float, image_size: int, device="cpu"):
        self._model = YOLO(str(model_path))
        self._confidence = confidence
        self._image_size = image_size
        self._device = device

    def detect(self, frame: Frame) -> tuple:
        try:
            result = self._model.predict(
                source=frame.image,
                imgsz=self._image_size,
                conf=self._confidence,
                verbose=False,
                device=self._device,
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


class RFDETRDetector:
    def __init__(self, model_path: Path, confidence: float, device: str):
        self._model = RFDETR.from_checkpoint(
            str(model_path), device=device, trust_checkpoint=True
        )
        self._confidence = confidence

    def detect(self, frame: Frame) -> tuple:
        try:
            rgb = cv2.cvtColor(frame.image, cv2.COLOR_BGR2RGB)
            result = self._model.predict(
                Image.fromarray(rgb), threshold=self._confidence, include_source_image=False
            )
            detections = []
            for index in range(len(result)):
                class_id = int(result.class_id[index])
                if class_id == len(self._model.class_names):
                    continue
                detection = Detection(
                    class_id=class_id,
                    label=self._model.class_names[class_id],
                    confidence=float(result.confidence[index]),
                    xyxy=tuple(result.xyxy[index].tolist()),
                )
                detections.append(detection)
            return tuple(detections)
        except (RuntimeError, ValueError, OSError, cv2.error) as error:
            raise AnalysisError("Local RF-DETR inference failed") from error
