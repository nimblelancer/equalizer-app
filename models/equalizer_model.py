from models.base_model import G2BaseModel
import numpy as np
from core.player.equalizer_service2 import EqualizerService2
import json
from config_manager import ConfigManager

class EqualizerModel(G2BaseModel):
    def __init__(self, eq_service: EqualizerService2, config_manager: ConfigManager, fs=44100):
        super().__init__()

        self.eq_service = eq_service
        self.config_manager = config_manager
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
        
        self.load_bands_from_json("eq_info_conf.json","edm")

        print(self.bands)

    def load_bands_from_json(self, file_path, genre):
        """Hàm này dùng để load các giá trị bands từ file JSON."""
        try:
            with open(file_path, 'r') as json_file:
                # Tải dữ liệu từ file JSON
                data = json.load(json_file)
                
                # Kiểm tra và gán lại cho self.bands
                if isinstance(data, dict):
                    self.bands = data[genre]
                else:
                    print("Dữ liệu không đúng định dạng trong file JSON.")
        except FileNotFoundError:
            print(f"File {file_path} không tồn tại.")
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

    def get_filter_coefficients(self):
        return self.eq_service.get_filter_coefficients()