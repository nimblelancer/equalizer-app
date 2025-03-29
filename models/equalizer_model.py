from models.base_model import G2BaseModel
import numpy as np
from core.player.equalizer_service2 import EqualizerService2
from core.player.noise_suppression_service import NoiseSuppressionService
import json
from config_manager import ConfigManager

class EqualizerModel(G2BaseModel):
    def __init__(self, eq_service: EqualizerService2, noise_service: NoiseSuppressionService, config_manager: ConfigManager, fs=44100):
        super().__init__()

        self.eq_service = eq_service
        self.config_manager = config_manager
        self.noise_service = noise_service
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
        
        self.load_bands_from_json("edm")

        print(self.bands)

        self.highcut_enabled = False
        self.lowcut_enabled = False
        self.amplitude_cut_enabled = False
        self.hum_cut_enabled = False
        self.bandstop_enabled = False
        self.bandnotch_enabled = False
        self.lms_enabled = False
        
        self.highcut_freq = 20000
        self.lowcut_freq = 20
        self.hum_freq = 60
        self.bandstop_list = []
        self.bandnotch_list = []
        self.q_factor = 20.0
        self.amplitude_cut = 100 

    def load_bands_from_json(self, genre):
        """Hàm này dùng để load các giá trị bands từ file JSON."""
        try:
            with open("eq_info_conf.json", 'r') as json_file:
                # Tải dữ liệu từ file JSON
                data = json.load(json_file)
                
                # Kiểm tra và gán lại cho self.bands
                if isinstance(data, dict):
                    self.bands = data[genre]
                else:
                    print("Dữ liệu không đúng định dạng trong file JSON.")
        except FileNotFoundError:
            print(f"File {json_file} không tồn tại.")
        except json.JSONDecodeError:
            print("Lỗi giải mã JSON. Hãy kiểm tra lại định dạng JSON trong file.")
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")

    def update_eq_info(self, eq_apply, bands, lowcut_freq, highcut_freq):
        """Cập nhật thông tin từ ViewModel về Equalizer"""
        self.eq_apply = eq_apply
        self.bands = bands
        self.lowcut_freq = lowcut_freq
        self.highcut_freq = highcut_freq

        self.eq_service.reset_filter_chain(self.lowcut_freq, self.highcut_freq, self.eq_apply, self.bands)

        self.notify_queued("eq_info_changed", {
                    "eq_apply": self.eq_apply,
                    "bands": self.bands,
                    "highcut_freq": self.highcut_freq,
                    "lowcut_freq": self.lowcut_freq
                })
        
    def update_noise_info(self,
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
            q_factor = 1.0,
            lms_enabled = False
            ):
        
        self.highcut_enabled = highcut_enabled
        self.lowcut_enabled = lowcut_enabled
        self.amplitude_cut_enabled = amplitude_cut_enabled
        self.hum_cut_enabled = hum_cut_enabled
        self.bandstop_enabled = bandstop_enabled
        self.bandnotch_enabled = bandnotch_enabled
        self.lms_enabled = lms_enabled
        
        self.highcut_freq = highcut_freq
        self.lowcut_freq = lowcut_freq
        self.hum_freq = hum_freq
        self.bandstop_list = bandstop_list
        self.bandnotch_list = bandnotch_list
        self.q_factor = q_factor
        self.amplitude_cut = amplitude_cut

        self.noise_service.reset_filter_chain(
            self.highcut_enabled,
            self.highcut_freq,
            self.lowcut_enabled,
            self.lowcut_freq,
            self.amplitude_cut_enabled,
            self.amplitude_cut,
            self.hum_cut_enabled,
            self.hum_freq,
            self.bandstop_enabled,
            self.bandstop_list,
            self.bandnotch_enabled,
            self.bandnotch_list,
            self.q_factor,
            self.lms_enabled
        )

        

        # self.notify_queued("noise_info_changed", {
        #             "eq_apply": self.eq_apply,
        #             "bands": self.bands,
        #             "highcut_freq": self.highcut_freq,
        #             "lowcut_freq": self.lowcut_freq
        #         })

    def get_filter_coefficients(self):
        return self.eq_service.get_filter_coefficients()