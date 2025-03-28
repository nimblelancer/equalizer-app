import numpy as np
from core.filter.filter_chain import FilterChain
from core.filter.filter_provider import FilterProvider
from core.filter.amplitude_cut_filter import AmplitudeCutFilter
from core.filter.lms_filter import LMSFilter
from scipy.io import wavfile

class NoiseSuppressionService:
    def __init__(self):
        self.fs = 44100
        self.filter_chain = FilterChain()
        self.filter_provider = FilterProvider()

    def reset_filter_chain(self,
            highcut_enabled = False,
            highcut_freq = 20000,
            lowcut_enabled = False,
            lowcut_freq = 20,
            amplitude_cut_enabled = False,
            amplitude_cut = 0.5,
            hum_cut_enabled = False,
            hum_freq = 60,
            bandstop_enabled = False,
            bandstop_list = [],
            bandnotch_enabled = False,
            bandnotch_list = [],
            q_factor = 30,
            lms_enabled = False
        ):
        self.filter_chain.reset_filter()
        if highcut_enabled:
            low_pass_filter = self.filter_provider.create_lowpass_filter(highcut_freq, filter_design="butter")
            self.filter_chain.add_filter(low_pass_filter, priority=20)
        if lowcut_enabled:
            high_pass_filter = self.filter_provider.create_highpass_filter(lowcut_freq, filter_design="butter")
            self.filter_chain.add_filter(high_pass_filter, priority=20)
        if amplitude_cut_enabled:
            amplitude_cut_filter = AmplitudeCutFilter(threshold=amplitude_cut)
            self.filter_chain.add_filter(amplitude_cut_filter, 1)
        if hum_cut_enabled:
            num_harmonics=5
            for i in range(1, num_harmonics + 1):
                harmonic_freq = hum_freq * i
                notch_filter = self.filter_provider.create_notch_filter(harmonic_freq, Q=q_factor, filter_design="butter")
                self.filter_chain.add_filter(notch_filter, priority=4)

        if bandnotch_enabled and len(bandnotch_list) > 0:
            for freq_ in bandnotch_list:
                notch_filter = self.filter_provider.create_notch_filter(freq_, Q=q_factor, filter_design="butter")
                self.filter_chain.add_filter(notch_filter, priority=4)
        if bandstop_enabled and len(bandstop_list) > 0:
            for lfreq_, hfreq_ in bandstop_list:
                bandstop_filter = self.filter_provider.create_bandstop_filter(lfreq_, hfreq_, filter_design="butter")
                self.filter_chain.add_filter(bandstop_filter, priority=4)

        if lms_enabled:
            mu = 0.01
            N = 32
            rate, r = wavfile.read('data/referenced_noise.wav') 
            lms_filter = LMSFilter(mu, N, r)  # Truyền tín hiệu tham chiếu khi khởi tạo
            self.filter_chain.add_filter(lms_filter, priority=4)


        print("number of noise filter:", self.filter_chain.filters)

    def suppress_noise(self, audio_data):
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

    