import numpy as np
from scipy.signal import butter, lfilter

class EqualizerService:
    def __init__(self):
        # Các dải tần số cho equalizer (Bass, Mid-bass, Midrange, Upper midrange, Treble)
        self.bands = {
            'Bass': (20, 200),
            'Mid-bass': (200, 500),
            'Midrange': (500, 2000),
            'Upper midrange': (2000, 5000),
            'Treble': (5000, 20000)
        }
    
    def apply_butter_filter(self, data, lowcut, highcut, fs, order=5):
        """Áp dụng bộ lọc Butterworth lên dữ liệu âm thanh"""
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        y = lfilter(b, a, data)
        return y
    
    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        """Tạo bộ lọc Butterworth dải (band-pass filter)"""
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_lowpass(self, cutoff, fs, order=4):
        """Tạo bộ lọc Butterworth lọc tần số cao (low-pass filter)"""
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='low')
        return b, a

    def butter_highpass(self, cutoff, fs, order=4):
        """Tạo bộ lọc Butterworth lọc tần số thấp (high-pass filter)"""
        nyquist = 0.5 * fs
        normal_cutoff = cutoff / nyquist
        b, a = butter(order, normal_cutoff, btype='high')
        return b, a

    

    def apply_band_filter(self, data, lowcut, highcut, fs):
        """Áp dụng bộ lọc dải lên dữ liệu âm thanh"""
        b, a = self.butter_bandpass(lowcut, highcut, fs)
        return lfilter(b, a, data)

    def apply_lowpass_filter(self, data, cutoff, fs):
        """Áp dụng bộ lọc low-pass lên dữ liệu âm thanh"""
        b, a = self.butter_lowpass(cutoff, fs)
        return lfilter(b, a, data)

    def apply_highpass_filter(self, data, cutoff, fs):
        """Áp dụng bộ lọc high-pass lên dữ liệu âm thanh"""
        b, a = self.butter_highpass(cutoff, fs)
        return lfilter(b, a, data)

    def equalize(self, audio_data, eq_apply, gains, lowcut=0, highcut=0, fs=44100):
        """
        Áp dụng bộ equalizer với các gain cho từng dải tần số và lọc nhiễu tần số thấp và cao.

        audio_data: Dữ liệu âm thanh cần equalizer.
        gains: Từ điển chứa mức gain cho từng dải tần số.
        lowcut: Tần số thấp mà chúng ta muốn lọc (dưới ngưỡng này sẽ bị cắt).
        highcut: Tần số cao mà chúng ta muốn lọc (trên ngưỡng này sẽ bị cắt).
        """

        # Chuyển đổi audio_data về float64 nếu nó không phải là kiểu này
        audio_data = np.asarray(audio_data, dtype=np.float64)

        if lowcut > 0:
            # Áp dụng high-pass filter để cắt nhiễu ở tần số thấp
            audio_data = self.apply_highpass_filter(audio_data, lowcut, fs)

        if highcut > 0:
            # Áp dụng low-pass filter để cắt nhiễu ở tần số cao
            audio_data = self.apply_lowpass_filter(audio_data, highcut, fs)

        if eq_apply:

            output = np.zeros_like(audio_data,dtype=np.float64)

            # Lọc và điều chỉnh mỗi dải tần số với mức gain tương ứng
            for band, (lcut, hcut) in self.bands.items():
                band_data = self.apply_band_filter(audio_data, lcut, hcut, fs)
                # Chuyển band_data về float64 để tránh lỗi kiểu dữ liệu khi cộng
                band_data = np.asarray(band_data, dtype=np.float64)
                band_data *= gains.get(band, 1)  # Áp dụng gain cho dải tần số
                output += band_data  # Tổng hợp các dải lại

            # Giới hạn giá trị âm thanh để tránh clipping (tức là âm thanh vượt qua giá trị tối đa hoặc tối thiểu)
            output = np.clip(output, -32768, 32767)

            return output
        
        else:
            return audio_data
