# 2. ViewModel: Quản lý kết nối giữa View và Model.
class NoiseSuppressionViewModel:
    def __init__(self, model):
        self.model = model
        # self.view = view  # Thêm tham chiếu đến view
        self.highcut_enabled = self.model.highcut_enabled
        self.lowcut_enabled = self.model.lowcut_enabled
        self.amplitude_cut_enabled = self.model.amplitude_cut_enabled
        self.hum_cut_enabled = self.model.hum_cut_enabled
        self.bandstop_enabled = self.model.bandstop_enabled
        self.bandnotch_enabled = self.model.bandnotch_enabled
        self.lms_enabled = self.model.lms_enabled
        self.highcut_freq = self.model.highcut_freq/100
        self.lowcut_freq = self.model.lowcut_freq
        self.hum_freq = self.model.hum_freq
        self.q_factor = self.model.q_factor
        self.amplitude_cut = self.model.amplitude_cut

    def update_model_from_view(self, 
            highcut_enabled,
            highcut_freq,
            lowcut_enabled,
            lowcut_freq,
            amplitude_cut_enabled,
            amplitude_cut,
            hum_cut_enabled,
            hum_freq,
            bandstop_enabled,
            bandstop_list,
            bandnotch_enabled,
            bandnotch_list,
            q_factor,
            lms_enabled):
        # Cập nhật model từ view

        print("update data here: ", highcut_enabled,
            highcut_freq,
            lowcut_enabled,
            lowcut_freq,
            amplitude_cut_enabled,
            amplitude_cut,
            hum_cut_enabled,
            hum_freq,
            bandstop_enabled,
            bandstop_list,
            bandnotch_enabled,
            bandnotch_list,
            q_factor,
            lms_enabled)
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
        self.q_factor = q_factor
        self.amplitude_cut = amplitude_cut
        self.bandstop_list = bandstop_list
        self.bandnotch_list = bandnotch_list

        self.model.update_noise_info(
            self.highcut_enabled,
            self.highcut_freq*100,
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

        # self.model.highcut_enabled = highcut_enabled
        # self.model.lowcut_enabled = lowcut_enabled
        # self.model.amplitude_cut_enabled = amplitude_cut_enabled
        # self.model.hum_cut_enabled = hum_cut_enabled
        # self.model.bandstop_enabled = bandstop_enabled
        # self.model.bandnotch_enabled = bandnotch_enabled
        # self.model.lms_enabled = lms_enabled
        # self.model.highcut_freq = highcut_freq
        # self.model.lowcut_freq = lowcut_freq
        # self.model.hum_freq = hum_freq
        # self.model.q_factor = q_factor
        # self.model.amplitude_cut = amplitude_cut

        print("val updated")

    def add_bandstop(self, freq):
        print(f'Freq: {freq} bandstop_list: {self.model.bandstop_list}')
        if freq and freq not in self.model.bandstop_list:
            self.model.bandstop_list.append(freq)

    def add_bandnotch(self, freq):
        if freq and freq not in self.model.bandnotch_list:
            self.model.bandnotch_list.append(freq)

    def remove_bandstop(self):
        self.model.bandstop_list.clear()
            

    def remove_bandnotch(self):
        self.model.bandnotch_list.clear()
            
    def get_filter_settings(self):
        return self.model.apply_filters()