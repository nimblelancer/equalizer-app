class NoiseSuppressionViewModel:
    def __init__(self, model):
        self.model = model
        # self.view = view  # Thêm tham chiếu đến view

    def update_model_from_view(self,highcut_var,lowcut_var,amplitude_cut_var,hum_cut_var,bandstop_var,bandnotch_var,lms_var,highcut_slider,lowcut_slider,hum_freq_slider,q_factor_slider,amplitude_cut_slider):
        # Cập nhật model từ view
        self.model.highcut_enabled = highcut_var
        self.model.lowcut_enabled = lowcut_var
        self.model.amplitude_cut_enabled = amplitude_cut_var
        self.model.hum_cut_enabled = hum_cut_var
        self.model.bandstop_enabled = bandstop_var
        self.model.bandnotch_enabled = bandnotch_var
        self.model.lms_enabled = lms_var

        self.model.highcut_freq = highcut_slider
        self.model.lowcut_freq = lowcut_slider
        self.model.hum_freq = hum_freq_slider
        self.model.q_factor = q_factor_slider
        self.model.amplitude_cut = amplitude_cut_slider

    def add_bandstop(self, freq):
        if freq and freq not in self.model.bandstop_list:
            self.model.bandstop_list.append(freq)

    def add_bandnotch(self, freq):
        if freq and freq not in self.model.bandnotch_list:
            self.model.bandnotch_list.append(freq)

    def remove_bandstop(self, freq):
        if freq in self.model.bandstop_list:
            self.model.bandstop_list.remove(freq)

    def remove_bandnotch(self, freq):
        if freq in self.model.bandnotch_list:
            self.model.bandnotch_list.remove(freq)

    def get_filter_settings(self):
        return self.model.apply_filters()
