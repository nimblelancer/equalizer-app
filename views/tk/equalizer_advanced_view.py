import tkinter as tk
from viewmodels.equalizer_advanced_viewmodel import EqualizerAdvancedViewModel
from views.tk.filter_freq_response_graphview import FilterFreqResponseGraphView

class EqualizerAdvancedView:
    def __init__(self, root, view_model: EqualizerAdvancedViewModel):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.view_model = view_model

        self.graph_view = FilterFreqResponseGraphView(self.frame)
        f, hs = self.view_model.get_frequency_response()
        self.graph_view.update_graph(f, hs)
        

        # Tạo các điều khiển cho dải tần số
        self.first_row_frame = tk.Frame(self.frame)
        self.first_row_frame.pack()

        self.band_controls = {}
        self.bands = self.view_model.bands  # Các tần số trung tâm, Q và Gain
        for band_name, params in self.bands.items():
            self.create_band_controls(band_name, params)

        self.view_model.add_view_listener(self)

    def create_band_controls(self, band_name, params, from_=20, to_=20000):
        band_frame = tk.Frame(self.first_row_frame)
        band_frame.pack(side=tk.LEFT, padx=5)

        label = tk.Label(band_frame, text=f"{band_name}")
        label.pack()

        # Tạo slider cho tần số
        freq_slider = tk.Scale(band_frame, from_=from_, to=to_, orient="horizontal", label="Frequency")
        freq_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        freq_slider.set(params['freq'])
        freq_slider.pack()

        # Tạo slider cho Q
        q_slider = tk.Scale(band_frame, from_=0.1, to=10, resolution=0.1, orient="horizontal", label="Q")
        q_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        q_slider.set(params['Q'])
        q_slider.pack()

        # Tạo slider cho Gain
        gain_slider = tk.Scale(band_frame, from_=-24, to=24, orient="horizontal", label="Gain (dB)")
        gain_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        gain_slider.set(params['gain'])
        gain_slider.pack()

        # Lưu thông tin của dải tần
        self.band_controls[band_name] = {
            'freq_slider': freq_slider,
            'q_slider': q_slider,
            'gain_slider': gain_slider,
        }

    def update_band_value(self, event=None):
        # Cập nhật các giá trị trong ViewModel khi người dùng thay đổi
        bands = {}
        for band_name, controls in self.band_controls.items():
            freq = controls['freq_slider'].get()
            Q = controls['q_slider'].get()
            gain = controls['gain_slider'].get()

            bands[band_name] = {'freq': freq, 'Q': Q, 'gain': gain}
        self.bands = bands
        self.view_model.update_band_values(self.bands)
        
    def update_view(self, event_name, data):
        if event_name == "eq_info_changed":
            print("eq_info_changed in equalizer_advanced_view")
            for band_name, controls in self.band_controls.items():
                controls['freq_slider'].set(self.view_model.bands[band_name]['freq'])
                controls['q_slider'].set(self.view_model.bands[band_name]['Q'])
                controls['gain_slider'].set(self.view_model.bands[band_name]['gain'])

            f, hs = self.view_model.get_frequency_response()
            self.graph_view.update_graph(f, hs)  # Cập nhật đồ thị khi có sự thay đổi
