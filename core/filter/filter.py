from scipy import signal

class Filter:
    def __init__(self, b, a):
        """Khởi tạo bộ lọc với các hệ số b và a."""
        self.b = b
        self.a = a

    def apply(self, audio_data):
        """Áp dụng bộ lọc lên tín hiệu âm thanh."""
        return signal.lfilter(self.b, self.a, audio_data)
    
    def get_coefficients(self):
        return self.b, self.a