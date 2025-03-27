import tkinter as tk
from tkinter import ttk
from viewmodels.equalizer_advanced_viewmodel import EqualizerAdvancedViewModel
from views.ttkbootstrap.filter_freq_response_graphview import FilterFreqResponseGraphView
import json
class EqualizerAdvancedView:
    def __init__(self, root, view_model: EqualizerAdvancedViewModel):
        self.frame = ttk.Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.view_model = view_model

        self.graph_view = FilterFreqResponseGraphView(self.frame)
        self.graph_view.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        f, hs = self.view_model.get_frequency_response()
        self.graph_view.update_graph(f, hs)

        # Frame chứa các điều khiển của Equalizer
        self.first_row_frame = ttk.Frame(self.frame)
        self.first_row_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Chia layout theo số lượng band
        self.first_row_frame.columnconfigure(tuple(range(len(self.view_model.bands))), weight=1)

        self.band_controls = {}
        self.bands = self.view_model.bands  # Các thông số: freq, Q, gain
        col = 0
        for band_name, params in self.bands.items():
            self.create_band_controls(band_name, params, col)
            col += 1

        
        # 🎯 Đọc dữ liệu từ file JSON
        with open("eq_info_conf.json", "r") as json_file:
            self.presets_data = json.load(json_file)

        # 🟢 Khung chứa radio buttons
        self.preset_frame = ttk.Frame(self.frame)
        self.preset_frame.grid(row=2, column=0, padx=10, pady=10)

        self.selected_preset = tk.StringVar(value=list(self.presets_data.keys())[0])  # Chọn preset đầu tiên

        preset_buttons = ttk.LabelFrame(self.preset_frame, text='Presets')
        preset_buttons.grid(row=0, column=1, padx=2)

        max_columns = 5
        row, col = 0, 0

        # Cấu hình cột để đảm bảo độ rộng bằng nhau
        for i in range(max_columns):
            preset_buttons.columnconfigure(i, weight=1, uniform="equal")

        # 🟡 Tạo các radio button và căn chỉnh ngay ngắn
        for preset in self.presets_data.keys():
            ttk.Radiobutton(
                preset_buttons, text=preset.capitalize(), value=preset, variable=self.selected_preset,
                bootstyle="primary", padding=(10, 3),
                command=self.apply_preset
            ).grid(row=row, column=col, padx=10, pady=5, sticky="w")  # 🔹 Căn trái chữ

            col += 1
            if col >= max_columns:  # Nếu đủ 5 preset thì xuống dòng mới
                col = 0
                row += 1
        self.reset_btn = ttk.Button(self.preset_frame, text="Reset", command=self.reset_preset, bootstyle='warning-outline')
        self.reset_btn.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.view_model.add_view_listener(self)
        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Hàm này sẽ được gọi khi cửa sổ bị đóng"""
        print("Closing Setting...")
        self.graph_view.on_close()
        self.view_model.on_close()

    def create_band_controls(self, band_name, params, col, from_=20, to_=20000):
        band_frame = ttk.LabelFrame(self.first_row_frame, text=band_name)
        band_frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

        # Cấu hình để kéo giãn theo cửa sổ
        band_frame.columnconfigure(0, weight=1)

        # Tạo slider cho Frequency
        freq_label = ttk.Label(band_frame, text="Frequency")
        freq_label.grid(row=0, column=0, padx=5, pady=2)
        freq_slider = ttk.Scale(band_frame, from_=from_, to=to_, orient="horizontal")
        freq_slider.grid(row=1, column=0, padx=5, pady=2, sticky="ew")
        freq_value_label = ttk.Label(band_frame, text=f"{params['freq']:.0f} Hz")
        freq_value_label.grid(row=1, column=1, padx=5, pady=2)
        freq_slider.bind("<Motion>", lambda event, label=freq_value_label: self.update_label(event, label, "Hz"))
        freq_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        freq_slider.set(params['freq'])

        # Tạo slider cho Q
        q_label = ttk.Label(band_frame, text="Q")
        q_label.grid(row=2, column=0, padx=5, pady=2)
        q_slider = ttk.Scale(band_frame, from_=0.1, to=10, orient="horizontal")
        q_slider.grid(row=3, column=0, padx=5, pady=2, sticky="ew")
        q_value_label = ttk.Label(band_frame, text=f"{params['Q']:.1f}")
        q_value_label.grid(row=3, column=1, padx=5, pady=2)
        q_slider.bind("<Motion>", lambda event, label=q_value_label: self.update_label(event, label, ""))
        q_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        q_slider.set(params['Q'])

        # Tạo slider cho Gain
        gain_label = ttk.Label(band_frame, text="Gain (dB)")
        gain_label.grid(row=4, column=0, padx=5, pady=2)
        gain_slider = ttk.Scale(band_frame, from_=-24, to=24, orient="horizontal")
        gain_slider.grid(row=5, column=0, padx=5, pady=2, sticky="ew")
        gain_value_label = ttk.Label(band_frame, text=f"{params['gain']:.1f} dB")
        gain_value_label.grid(row=5, column=1, padx=5, pady=2)
        gain_slider.bind("<Motion>", lambda event, label=gain_value_label: self.update_label(event, label, "dB"))
        gain_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        gain_slider.set(params['gain'])

        # Lưu thông tin dải tần
        self.band_controls[band_name] = {
            'freq_slider': freq_slider,
            'q_slider': q_slider,
            'gain_slider': gain_slider,
            'freq_value_label': freq_value_label,
            'q_value_label': q_value_label,
            'gain_value_label': gain_value_label,
        }

    def update_label(self, event, label, unit):
        """Cập nhật giá trị của label khi di chuyển slider"""
        value = event.widget.get()
        label.config(text=f"{value:.1f} {unit}".strip())

    def update_band_value(self, event=None):
        """Cập nhật các giá trị trong ViewModel khi người dùng thay đổi"""
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

                controls['freq_value_label'].config(text=f"{self.view_model.bands[band_name]['freq']:.0f} Hz")
                controls['q_value_label'].config(text=f"{self.view_model.bands[band_name]['Q']:.1f}")
                controls['gain_value_label'].config(text=f"{self.view_model.bands[band_name]['gain']:.1f} dB")

            f, hs = self.view_model.get_frequency_response()
            self.graph_view.update_graph(f, hs)  # Cập nhật đồ thị khi có sự thay đổi

    def apply_preset(self):
        """Update all band parameters based on the selected preset"""
        self.view_model.apply_equalizer_advanced_preset(self.selected_preset.get().lower())

    def reset_preset(self):
        self.bands = self.view_model.bands
        self.view_model.update_band_values(self.bands)