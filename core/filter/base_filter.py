from abc import ABC, abstractmethod

class G2Filter(ABC):
    @abstractmethod
    def apply(self, audio_data):
        pass