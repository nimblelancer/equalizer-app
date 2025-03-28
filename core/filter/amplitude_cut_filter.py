import numpy as np

class AmplitudeCutFilter:
    def __init__(self, threshold, window_size=5):
        self.threshold = threshold
        self.window_size = window_size

    
    def apply(self, signal):
        # # Chuyển tín hiệu thành mảng NumPy nếu không phải là mảng NumPy
        # signal = np.array(signal)
        # print(signal, self.threshold)
        
        # # Thực hiện cắt biên độ
        # signal[np.abs(signal) < self.threshold] = 0
        # Cắt biên độ nhỏ hơn threshold
        filtered_signal = np.copy(signal)
        filtered_signal[np.abs(filtered_signal) < self.threshold] = 0
        
        # Áp dụng smoothing (moving average) cho tín hiệu đã cắt
        smoothed_signal = self.smooth(filtered_signal)
        
        return smoothed_signal
    
    def smooth(self, signal):
        # Hàm smoothing (moving average)
        smoothed_signal = np.copy(signal)
        for i in range(self.window_size, len(signal) - self.window_size):
            smoothed_signal[i] = np.mean(signal[i - self.window_size:i + self.window_size])
        return smoothed_signal