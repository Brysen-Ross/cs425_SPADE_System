import cv2
import numpy as np
import urllib.request

class Camera:
    def __init__(self, url="http://127.0.0.1:8081/snapshot"):
        self.url = url
        self.frame = None
        self.connected = False
    
    def connect(self):
        self.frame = self.get_frame()
        self.connected = self.frame is not None
        return self.connected

    def get_frame(self):
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

    def disconnect(self):
        self.connected = False
        self.frame = None