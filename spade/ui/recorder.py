from pathlib import Path
from datetime import datetime
from threading import Thread, Event
from time import sleep
import cv2
import mss
import numpy as np


class WindowRecorder:
    def __init__(self, output_folder, fps=10):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.fps = fps
        self.stop_event = Event()
        self.thread = None
        self.writer = None
        self.output_path = None

        self.region = None

    def start(self, region):
        if self.thread is not None:
            return

        self.region = region

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_path = self.output_folder / f"SPADE_UI_{timestamp}.mp4"

        self.thread = Thread(target=self._record_loop, daemon=True)
        self.thread.start()

    def _record_loop(self):
        frame_delay = 1 / self.fps

        with mss.mss() as sct:
            while not self.stop_event.is_set():
                if self.region is None:
                    sleep(frame_delay)
                    continue

                monitor = {"top": self.region["top"], "left": self.region["left"], "width": self.region["width"], "height": self.region["height"],}

                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                if self.writer is None:
                    height, width = frame.shape[:2]
                    self.writer = cv2.VideoWriter(
                        str(self.output_path),
                        cv2.VideoWriter_fourcc(*"mp4v"),
                        self.fps,
                        (width, height)
                    )

                    if not self.writer.isOpened():
                        raise RuntimeError(f"Could not create recording file: {self.output_path}")

                self.writer.write(frame)
                sleep(frame_delay)

        if self.writer is not None:
            self.writer.release()
            self.writer = None

    def stop(self):
        if self.thread is None:
            return

        self.stop_event.set()
        self.thread.join(timeout=3)
        self.thread = None