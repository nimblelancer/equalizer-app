from models.equalizer_model import EqualizerModel
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from viewmodels.base_viewmodel import G2BaseViewModel

class EqualizerViewModel2(G2BaseViewModel):
    def __init__(self, model: EqualizerModel):
        super().__init__(model)

        self.model = model
        self.model.add_listener("filter_coeff_changed", self)

        self.fs = 44100
        self.eq_apply = True
        self.bands = {
            'Bass': {'freq': 50, 'Q': 1.0, 'gain': 0},
            'Mid-bass': {'freq': 200, 'Q': 1.0, 'gain': 0},
            'Midrange': {'freq': 1000, 'Q': 1.0, 'gain': 0},
            'Upper Mid': {'freq': 3000, 'Q': 1.0, 'gain': 0},
            'Treble': {'freq': 8000, 'Q': 1.0, 'gain': 0},
        }
        self.low_cut = True
        self.high_cut = True
        self.lowcut_freq = 20
        self.highcut_freq = 20

        # Khởi tạo bộ lọc với các đỉnh
        self.b_total_peak = np.array([1])  # Hệ số b (số) của Peaking
        self.a_total_peak = np.array([1])  # Hệ số a (mẫu) của Peaking

        # self.update_equalizer_info(self.eq_apply, 0, 0, 0, 0, 0, self.low_cut, self.lowcut_freq, self.high_cut, self.highcut_freq)


    def update_equalizer_info(self, eq_apply, bass_gain, midbass_gain, midrange_gain, uppermid_gain, treeble_gain, lowcut_applied, lowcut_freq, highcut_applied, highcut_freq):
        """Cập nhật giá trị bộ equalizer vào AudioPlayerModel"""
        gains = {
            'Bass': bass_gain,  # Tăng bass
            'Mid-bass': midbass_gain,  # Giữ nguyên mid-bass
            'Midrange': midrange_gain,  # Giảm midrange
            'Upper midrange': uppermid_gain,  # Giữ nguyên upper midrange
            'Treble': treeble_gain  # Tăng treble
        }

        if not self.low_cut:
            self.lowcut_freq = 0
        
        if not self.high_cut:
            self.highcut_freq = 0

        self.model.update_eq_info(self.eq_apply, self.bands, self.lowcut_freq, self.highcut_freq*1000)
        
        print(self.model.eq_apply, self.model.bands, self.model.lowcut_freq, self.model.highcut_freq)

    def update_band_values(self, bands):
        # print("update_band_value")
        self.bands = bands
        self.model.update_eq_info(self.eq_apply, self.bands, self.lowcut_freq, self.highcut_freq*1000)

    def get_frequency_response(self):
        # Tạo mảng tần số từ 20 Hz đến 20 kHz để kiểm tra đáp ứng tần số
        
        f = np.logspace(np.log10(1), np.log10(22000), 500)
        hs = []
        for ab in self.model.get_filter_coefficients():
            w, h = signal.freqz(ab["b"], ab["a"], worN=2 * np.pi * f / self.fs)
            hs.append(h)
        return f, hs