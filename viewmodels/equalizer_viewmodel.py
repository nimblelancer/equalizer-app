from models.audio_player_model import AudioPlayerModel

class EqualizerViewModel:
    def __init__(self, model: AudioPlayerModel):
        self.model = model

    def update_equalizer_info(self, eq_apply, bass_gain, midbass_gain, midrange_gain, uppermid_gain, treeble_gain, lowcut_applied, lowcut_freq, highcut_applied, highcut_freq, filter_type, notch_apply, notch_low, notch_high):
        """Cập nhật giá trị bộ equalizer vào AudioPlayerModel"""

        self.model.eq_apply = eq_apply
        self.model.filter_type = filter_type
        self.model.notch_apply = notch_apply

        self.model.gains = {
            'Bass': bass_gain,  # Tăng bass
            'Mid-bass': midbass_gain,  # Giữ nguyên mid-bass
            'Midrange': midrange_gain,  # Giảm midrange
            'Upper midrange': uppermid_gain,  # Giữ nguyên upper midrange
            'Treble': treeble_gain  # Tăng treble
        }
        if lowcut_applied:
            self.model.lowcut_freq = lowcut_freq
        else:
            self.model.lowcut_freq = 0
        
        if highcut_applied:
            self.model.highcut_freq =highcut_freq*1000
        else:
            self.model.highcut_freq = 0

        if notch_low: 
            self.model.notch_low = notch_low
        else:
            self.model.notch_low = 0

        if notch_high: 
            self.model.notch_high = notch_high
        else:
            self.model.notch_high = 0

        print(f'Apply Equalizer: {self.model.eq_apply}, Gains: {self.model.gains}, Lowcut: {self.model.lowcut_freq}, Highcut: {self.model.highcut_freq}, Filter Type: {self.model.filter_type}, Notch Apply: {self.model.notch_apply}, Notch Low: {self.model.notch_low}, Notch High: {self.model.notch_high}')
        