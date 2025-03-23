import numpy as np
from scipy.signal import butter, lfilter
from viewmodels.base_viewmodel import G2BaseViewModel
from models.audio_player_model import AudioPlayerModel

class AudioGraphViewModel(G2BaseViewModel):
    def __init__(self, model: AudioPlayerModel):
        super().__init__(model)
        self.model.add_listener("audio_chunk_changed", self)

        self.original_audio_data = None
        self.filtered_audio_data = None

    def toggle_graph(self, is_show):
        self.model.show_graph = is_show

    def update_audio_data(self, original_audio_data, filtered_audio_data):
        """Cập nhật dữ liệu âm thanh cho View"""
        self.original_audio_data = original_audio_data
        self.filtered_audio_data = filtered_audio_data

    def butter_bandpass(self, lowcut, highcut, order=4):
        nyquist = 0.5 * 44100
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def apply_filter(self, data, lowcut, highcut):
        b, a = self.butter_bandpass(lowcut, highcut)
        return lfilter(b, a, data)

    def get_audio_data(self):
        t = np.linspace(0, 1, 44100)
        self.original_audio_data = np.sin(2 * np.pi * 100 * t) + np.sin(2 * np.pi * 500 * t)  # Sóng 100Hz và 500Hz
        self.filtered_audio_data = self.apply_filter(self.original_audio_data, lowcut=150, highcut=1000)


        return self.original_audio_data, self.filtered_audio_data
