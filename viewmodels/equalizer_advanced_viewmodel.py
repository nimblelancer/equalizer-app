from models.equalizer_model import EqualizerModel
import numpy as np
from scipy import signal
from viewmodels.base_viewmodel import G2BaseViewModel

class EqualizerAdvancedViewModel(G2BaseViewModel):
    def __init__(self, model: EqualizerModel):
        super().__init__(model)

        self.model.add_listener("eq_info_changed", self)
        # self.model.add_listener("filter_coeff_changed", self)
        
        self.fs = self.model.fs
        self.eq_apply = self.model.eq_apply
        self.bands = self.model.bands
        self.lowcut_apply = self.model.lowcut_freq > 0
        self.highcut_apply = self.model.highcut_freq > 0
        self.lowcut_freq = self.model.lowcut_freq if self.model.lowcut_freq > 0 else 20
        self.highcut_freq = self.model.highcut_freq/1000 if self.model.highcut_freq > 0 else 20

        # Khởi tạo bộ lọc với các đỉnh
        self.b_total_peak = np.array([1])  # Hệ số b (số) của Peaking
        self.a_total_peak = np.array([1])  # Hệ số a (mẫu) của Peaking

    def update_band_values(self, bands):
        # print("update_band_value")
        self.bands = bands
        self.model.update_eq_info(self.eq_apply, self.bands, self.model.lowcut_freq, self.model.highcut_freq)

    def get_frequency_response(self):
        # Tạo mảng tần số từ 20 Hz đến 20 kHz để kiểm tra đáp ứng tần số
        
        f = np.logspace(np.log10(1), np.log10(22000), 500)
        hs = []
        for ab in self.model.get_filter_coefficients():
            w, h = signal.freqz(ab["b"], ab["a"], worN=2 * np.pi * f / self.fs)
            hs.append(h)
        return f, hs
    
    def on_notify(self, event_name, data):
        if event_name == "eq_info_changed":
            print("eq_info_changed in equalizer_advanced_viewmodel")
            self.eq_apply = self.model.eq_apply
            self.bands = self.model.bands
            self.lowcut_apply = self.model.lowcut_freq > 0
            self.highcut_apply = self.model.highcut_freq > 0
            self.lowcut_freq = self.model.lowcut_freq if self.model.lowcut_freq > 0 else 20
            self.highcut_freq = self.model.highcut_freq/1000 if self.model.highcut_freq > 0 else 20
            self.notify_view(event_name, None)
        else:
            super().notify_view(event_name, data)  # Gọi hàm super