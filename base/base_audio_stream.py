from abc import ABC, abstractmethod

class G2AudioStream(ABC):
    """Wrapper chung cho các thư viện âm thanh"""
    
    @abstractmethod
    def start_stream(self):
        pass

    @abstractmethod
    def stop_stream(self):
        pass

    @abstractmethod
    def write(self, data):
        pass

    @abstractmethod
    def read(self, chunk_size):
        pass

    @abstractmethod
    def close(self):
        pass
