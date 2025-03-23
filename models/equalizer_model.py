from models.base_model import G2BaseModel
import numpy as np
from core.player.equalizer_service2 import EqualizerService2

class EqualizerModel(G2BaseModel):
    def __init__(self, eq_service: EqualizerService2, fs=44100):
        super().__init__()

        self.eq_service = eq_service
        self.fs = fs
        self.eq_apply = False
        # self.gains = {}
        self.lowcut_freq = 0
        self.highcut_freq = 0
        self.freq_ranges = [(20, 300), (150, 600), (400, 1200), (900, 6000), (5000, 20000)]
        self.bands = {
            'Bass': {'freq': 50, 'Q': 1.0, 'gain': 0},
            'Mid-bass': {'freq': 200, 'Q': 1.0, 'gain': 0},
            'Midrange': {'freq': 1000, 'Q': 1.0, 'gain': 0},
            'Upper Mid': {'freq': 3000, 'Q': 1.0, 'gain': 0},
            'Treble': {'freq': 8000, 'Q': 1.0, 'gain': 0},
        }

    def update_eq_info(self, eq_apply, bands, lowcut_freq, highcut_freq):
        """Cập nhật thông tin từ ViewModel về Equalizer"""
        self.eq_apply = eq_apply
        self.bands = bands
        self.lowcut_freq = lowcut_freq
        self.highcut_freq = highcut_freq

        self.eq_service.reset_filter_chain(self.lowcut_freq, self.highcut_freq, self.eq_apply, self.bands)

        self.notify_queued("filter_coeff_changed", {
                    "filter_coeffs": self.eq_service.get_filter_coefficients()
                })
        
    def get_filter_coefficients(self):
        return self.eq_service.get_filter_coefficients()