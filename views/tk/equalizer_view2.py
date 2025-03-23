import tkinter as tk
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from views.filter_freq_response_graphview import FilterFreqResponseGraphView

class EqualizerView2:
    def __init__(self, root, view_model: EqualizerViewModel2):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.view_model = view_model

        # Khởi tạo FrequencyResponseGraph để vẽ đồ thị
        self.frequency_response_graph = FilterFreqResponseGraphView(self.frame, self.view_model)

        # Các điều khiển dải tần số (Frequency, Q, Gain)
        self.band_controls = {}
        self.first_row_frame = tk.Frame(self.frame)
        self.first_row_frame.pack()

        self.bands = self.view_model.bands  # Lấy dải tần từ view model
        for band_name, params in self.bands.items():
            self.create_band_controls(band_name, params)

        # Lắng nghe sự thay đổi từ view model
        self.view_model.add_view_listener(self)

    def create_band_controls(self, band_name, params, from_=20, to_=20000):
        band_frame = tk.Frame(self.first_row_frame)
        band_frame.pack(side=tk.LEFT, padx=5)

        label = tk.Label(band_frame, text=f"{band_name}")
        label.pack()

        # Tạo slider cho tần số
        freq_slider = tk.Scale(band_frame, from_=from_, to=to_, orient="horizontal", label="Frequency")
        freq_slider.set(params['freq'])
        freq_slider.pack()

        # Tạo slider cho Q
        q_slider = tk.Scale(band_frame, from_=0.1, to=10, resolution=0.1, orient="horizontal", label="Q")
        q_slider.set(params['Q'])
        q_slider.pack()

        # Tạo slider cho Gain
        gain_slider = tk.Scale(band_frame, from_=-24, to=24, orient="horizontal", label="Gain (dB)")
        gain_slider.set(params['gain'])
        gain_slider.pack()

        # Lưu thông tin của dải tần
        self.band_controls[band_name] = {
            'freq_slider': freq_slider,
            'q_slider': q_slider,
            'gain_slider': gain_slider,
        }

        # Gắn callback cập nhật giá trị khi người dùng thay đổi
        freq_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_values())
        q_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_values())
        gain_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_values())

    def update_band_values(self):
        """Cập nhật các giá trị band trong view model khi người dùng thay đổi"""
        bands = {}
        for band_name, controls in self.band_controls.items():
            freq = controls['freq_slider'].get()
            Q = controls['q_slider'].get()
            gain = controls['gain_slider'].get()
            bands[band_name] = {'freq': freq, 'Q': Q, 'gain': gain}
        self.view_model.update_band_values(bands)

    def update_view(self, event_name, data):
        """Cập nhật đồ thị khi có sự thay đổi trong filter coefficients"""
        if event_name == "filter_coeff_changed":
            self.frequency_response_graph.update_graph()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
