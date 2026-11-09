from pathlib import Path
from urllib.request import Request, urlopen

import cv2
import numpy as np

from .models import Frame


class HttpSnapshotSource:
    def __init__(self, url: str):
        self.url = url
        self.connected = False
        self.fps = 30.0

    def connect(self) -> bool:
        return self.read() is not None

    def read(self):
        try:
            request = Request(self.url, headers={"Cache-Control": "no-cache"})
            with urlopen(request, timeout=2) as response:
                data = np.frombuffer(response.read(), dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)
            self.connected = image is not None
            return Frame(image) if image is not None else None
        except (OSError, ValueError, cv2.error) as error:
            print("Camera error:", error)
            self.connected = False
            return None

    def disconnect(self) -> None:
        self.connected = False


class VideoFileSource:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.fps = 30.0
        self._capture = None

    @property
    def connected(self) -> bool:
        return self._capture is not None and self._capture.isOpened()

    def connect(self) -> bool:
        if self.connected:
            return True
        self.disconnect()
        self._capture = cv2.VideoCapture(str(self.path))
        if not self.connected:
            self.disconnect()
            return False
        fps = self._capture.get(cv2.CAP_PROP_FPS)
        self.fps = fps if 0 < fps <= 240 else 30.0
        return True

    def read(self):
        if not self.connected:
            return None
        success, image = self._capture.read()
        if not success:
            self.disconnect()
            if not self.connect():
                return None
            success, image = self._capture.read()
        if not success:
            self.disconnect()
            return None
        return Frame(image)

    def disconnect(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None
