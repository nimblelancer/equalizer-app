import numpy as np
from core.filter.filter_chain import FilterChain
from core.filter.filter_provider import FilterProvider

FILTER_ORDER = 4

class EqualizerService2:

    def __init__(self):
        # self.audio_dim = 2
        self.fs = 44100
        self.filter_chain = FilterChain()
        self.filter_provider = FilterProvider()

    def reset_audio(self, fs, dim):
        self.fs = fs
        # self.audio_dim = dim

    def reset_filter_chain(self, low_cut, high_cut, eq_apply, bands):
        self.filter_chain.reset_filter()
        if low_cut > 0:
            high_pass_filter = self.filter_provider.create_highpass_filter(low_cut, filter_design="butter")
            self.filter_chain.add_filter(high_pass_filter, priority=2)
        if high_cut > 0:
            low_pass_filter = self.filter_provider.create_lowpass_filter(high_cut, filter_design="butter")
            self.filter_chain.add_filter(low_pass_filter, priority=1)
        if eq_apply:
            peak_filter = self.filter_provider.create_peak_filter(bands, filter_design="custom")
            self.filter_chain.add_filter(peak_filter, priority=3)

    def equalize(self, audio_data):
        # Nếu filter chain bị rỗng thì không xử lý gì
        if self.filter_chain.is_empty():
            return audio_data
        # Nếu dữ liệu âm thanh là stereo (2 kênh), xử lý từng kênh riêng biệt
        if audio_data.ndim == 2:  # Stereo
            output_left = self.filter_chain.apply(audio_data[:, 0])
            output_right = self.filter_chain.apply(audio_data[:, 1])
            return np.vstack((output_left, output_right)).T
        else:  # Mono, chỉ có 1 kênh
            return self.filter_chain.apply(audio_data)
        
    def get_filter_coefficients(self):
        return self.filter_chain.get_coefficients()
