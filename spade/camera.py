
import cv2
import numpy as np
import urllib.request
from pathlib import Path
from time import perf_counter
from ultralytics import YOLO

class Camera:
    def __init__(
        self,
        url="http://127.0.0.1:8081/snapshot",
        model_path=None,
        confidence=0.75,
        image_size=512
    ):
        self.url = url
        self.frame = None
        self.connected = False
        self.capture = None

        self.model = YOLO(str(model_path)) if model_path else None
        self.confidence = confidence
        self.image_size = image_size

        self.paused = False
        self.failure_detected = False
        self.frame_number = 0
        self.video_fps = 30.0
        self.cooldown_until_frame = 0

    def connect(self):
        if Path(self.url).is_file():
            self.capture = cv2.VideoCapture(self.url)
            self.connected = self.capture.isOpened()

            if self.connected:
                fps = self.capture.get(cv2.CAP_PROP_FPS)
                if 0 < fps <= 240:
                    self.video_fps = fps

            return self.connected

        self.frame = self.get_frame()
        self.connected = self.frame is not None
        return self.connected

    def get_frame(self):
        if self.paused:
            return self.frame
        if self.capture is not None:
            success, frame = self.capture.read()

            if not success:
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                success, frame = self.capture.read()

            if success:
                self.frame_number += 1
                return self.analyze_frame(frame)

            self.connected = False
            return None

        try:
            request = urllib.request.Request(self.url, headers={"Cache-Control": "no-cache"})

            with urllib.request.urlopen(request, timeout=2) as response:
                data = response.read()
                image = np.frombuffer(data, dtype=np.uint8)
                frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
                return frame

        except (OSError, ValueError, cv2.error) as error:
            print("Camera error:", error)
            self.connected = False
            return None



    def analyze_frame(self, frame):
        if self.model is None:
            self.frame = frame
            return frame

        start = perf_counter()

        result = self.model.predict(
            source=frame,
            imgsz=self.image_size,
            conf=self.confidence,
            verbose=False
        )[0]

        inference_ms = (perf_counter() - start) * 1000

        boxes = result.boxes
        self.failure_detected = (
            boxes is not None and len(boxes) > 0
        )

        self.frame = result.plot()

        if self.failure_detected:
            confidence = max(
                float(box.conf[0]) for box in boxes
            )

            video_time = self.frame_number / self.video_fps

            print(
                f"Detection at {video_time:.2f}s | "
                f"Confidence: {confidence:.1%} | "
                f"Inference: {inference_ms:.1f} ms"
            )

            if self.frame_number >= self.cooldown_until_frame:
                self.paused = True
                print("SPADE: Failure detected - video paused.")

        return self.frame

    def resume(self):
        if self.paused:
            self.paused = False
            self.failure_detected = False

            # Allow one second of source-video playback
            # before another automatic pause.
            self.cooldown_until_frame = (
                self.frame_number + round(self.video_fps)
            )

            print("SPADE: Video resumed.")



    def disconnect(self):
        self.paused = False
        if self.capture is not None:
            self.capture.release()
            self.capture = None

        self.connected = False
        self.frame = None