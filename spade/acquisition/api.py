from abc import ABC, abstractmethod

from .models import Frame


class FrameSource(ABC):
    @property
    @abstractmethod
    def connected(self) -> bool:
        pass

    @property
    @abstractmethod
    def fps(self) -> float:
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
