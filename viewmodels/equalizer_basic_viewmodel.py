from models.equalizer_model import EqualizerModel
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from viewmodels.base_viewmodel import G2BaseViewModel
# from di_container import DiContainer

class EqualizerBasicViewModel(G2BaseViewModel):
    def __init__(self, model: EqualizerModel):
        super().__init__(model)

        self.model.add_listener("eq_info_changed", self)
        # self.model.add_listener("filter_coeff_changed", self)
        # container = DiContainer()
        # container.audio_player_model().add_listener("audio_stream_changed", self)

        self.fs = self.model.fs

        self.eq_apply = self.model.eq_apply
        self.lowcut_apply = self.model.lowcut_freq > 0
        self.highcut_apply = self.model.highcut_freq > 0

        self.band_gains = {band: self.model.bands[band]['gain'] for band in self.model.bands}

        self.lowcut_freq = self.model.lowcut_freq if self.model.lowcut_freq > 0 else 20
        self.highcut_freq = self.model.highcut_freq/1000 if self.model.highcut_freq > 0 else 20

    def update_equalizer_info(self, eq_apply, gains, lowcut_applied, lowcut_freq, highcut_applied, highcut_freq):
        
        self.eq_apply = eq_apply
        self.lowcut_apply = lowcut_applied
        self.highcut_apply = highcut_applied
        self.band_gains = gains

        bands = self.model.bands
        for band in bands:
            bands[band]['gain'] = gains[band]

        if not self.lowcut_apply:
            self.lowcut_freq = 0
        else:
            self.lowcut_freq = lowcut_freq
        
        if not self.highcut_apply:
            self.highcut_freq = 0
        else:
            self.highcut_freq = highcut_freq

        self.model.update_eq_info(self.eq_apply, bands, self.lowcut_freq, self.highcut_freq*1000)

        print(self.model.eq_apply, self.model.bands, self.model.lowcut_freq, self.model.highcut_freq)

    def on_notify(self, event_name, data):
        if event_name == "eq_info_changed":
            print("eq_info_changed in equalizer_basic_viewmodel")
            self.eq_apply = self.model.eq_apply
            self.lowcut_apply = self.model.lowcut_freq > 0
            self.highcut_apply = self.model.highcut_freq > 0

            self.band_gains = {band: self.model.bands[band]['gain'] for band in self.model.bands}

            self.lowcut_freq = self.model.lowcut_freq if self.model.lowcut_freq > 0 else 20
            self.highcut_freq = self.model.highcut_freq/1000 if self.model.highcut_freq > 0 else 20
            self.notify_view(event_name, None)
        else:
            super().notify_view(event_name, data)  # Gọi hàm super

        