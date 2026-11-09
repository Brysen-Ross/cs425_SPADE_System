from typing import Protocol

from .models import Frame


class FrameSource(Protocol):
    @property
    def connected(self) -> bool:
        pass

    @property
    def fps(self) -> float:
        pass

    def connect(self) -> bool:
        pass

    def read(self):
        pass

    def disconnect(self) -> None:
        pass
