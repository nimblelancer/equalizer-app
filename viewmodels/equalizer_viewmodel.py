from models.audio_player_model import AudioPlayerModel
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class EqualizerViewModel:
    def __init__(self, model: AudioPlayerModel):
        self.model = model

        self.fs = 44100

        # Các dải tần số (bao gồm tần số trung tâm, Q và Gain)
        self.bands = {
            'Bass': {'freq': 50, 'Q': 1.0, 'gain': 0},
            'Mid-bass': {'freq': 200, 'Q': 1.0, 'gain': 0},
            'Midrange': {'freq': 1000, 'Q': 1.0, 'gain': 0},
            'Upper Mid': {'freq': 3000, 'Q': 1.0, 'gain': 0},
            'Treble': {'freq': 8000, 'Q': 1.0, 'gain': 0},
        }

        # Khởi tạo bộ lọc với các đỉnh
        self.b_total_peak = np.array([1])  # Hệ số b (số) của Peaking
        self.a_total_peak = np.array([1])  # Hệ số a (mẫu) của Peaking

    def update_equalizer_info(self, eq_apply, bass_gain, midbass_gain, midrange_gain, uppermid_gain, treeble_gain, lowcut_applied, lowcut_freq, highcut_applied, highcut_freq):
        """Cập nhật giá trị bộ equalizer vào AudioPlayerModel"""
        gains = {
            'Bass': bass_gain,  # Tăng bass
            'Mid-bass': midbass_gain,  # Giữ nguyên mid-bass
            'Midrange': midrange_gain,  # Giảm midrange
            'Upper midrange': uppermid_gain,  # Giữ nguyên upper midrange
            'Treble': treeble_gain  # Tăng treble
        }

        if not lowcut_applied:
            lowcut_freq = 0
        
        if not highcut_applied:
            highcut_freq = 0

        self.model.set_eq_applied(eq_apply, gains, lowcut_freq*1000, highcut_freq*1000)

        print(self.model.eq_apply, self.model.gains, self.model.lowcut_freq, self.model.highcut_freq)

    def peaking_filter(self, f0, Q, gain):
        omega0 = 2 * np.pi * f0 / self.fs  # Tần số góc trung tâm
        alpha = np.sin(omega0) / (2 * Q)

        A = 10 ** (gain / 40)  # Độ khuếch đại

        b0 = 1 + alpha * A
        b1 = -2 * np.cos(omega0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(omega0)
        a2 = 1 - alpha / A
        
        b = np.array([b0, b1, b2]) / a0
        a = np.array([a0, a1, a2]) / a0
        return b, a

    def generate_peak_filter(self):
        # Tạo bộ lọc Peaking Equalizer cho các dải tần số
        self.b_total_peak = np.array([1])
        self.a_total_peak = np.array([1])

        for band_name, params in self.bands.items():
            f0 = params['freq']
            Q = params['Q']
            gain = params['gain']
            
            # Tạo bộ lọc Peaking và cộng dồn
            b, a = self.peaking_filter(f0, Q, gain)
            self.b_total_peak = np.convolve(self.b_total_peak, b)
            self.a_total_peak = np.convolve(self.a_total_peak, a)

    def get_frequency_response(self):
        # Tạo mảng tần số từ 20 Hz đến 20 kHz để kiểm tra đáp ứng tần số
        f = np.logspace(np.log10(1), np.log10(22000), 500)

        # Tính đáp ứng tần số của bộ lọc Peaking Equalizer
        w_peaking, h_peaking = signal.freqz(self.b_total_peak, self.a_total_peak, worN=2 * np.pi * f / self.fs)

        # Thiết kế bộ lọc Butterworth cắt tần số thấp (Highpass) dưới 20 Hz
        highpass_b, highpass_a = signal.butter(4, 20, 'high', fs=self.fs)

        # Thiết kế bộ lọc Butterworth cắt tần số cao (Lowpass) dưới 20 kHz
        lowpass_b, lowpass_a = signal.butter(4, 20000, 'low', fs=self.fs)

        # Tính đáp ứng tần số của bộ lọc Highpass
        w_hp, h_hp = signal.freqz(highpass_b, highpass_a, worN=2 * np.pi * f / self.fs)

        # Tính đáp ứng tần số của bộ lọc Lowpass
        w_lp, h_lp = signal.freqz(lowpass_b, lowpass_a, worN=2 * np.pi * f / self.fs)

        return f, h_peaking, h_hp, h_lp
        
        