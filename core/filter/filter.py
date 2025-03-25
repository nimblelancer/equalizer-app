from scipy import signal
import numpy as np
class Filter:
    def __init__(self, b, a):
        """Khởi tạo bộ lọc với các hệ số b và a."""
        self.b = b
        self.a = a
        self.filter_state = np.zeros(len(a) - 1)

    def apply(self, audio_data):
        """Áp dụng bộ lọc lên tín hiệu âm thanh."""
        y, self.filter_state = signal.lfilter(self.b, self.a, audio_data, zi=self.filter_state)
        return y
    
    def get_coefficients(self):
        return self.b, self.a