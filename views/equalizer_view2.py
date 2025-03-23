import tkinter as tk
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from tkinter import Toplevel
from scipy import signal
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class EqualizerView2:
    def __init__(self, root, view_model: EqualizerViewModel2):
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Khởi tạo ViewModel
        self.view_model = view_model
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.setup_axs()

        # Hiển thị đồ thị trên Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)  # Tạo canvas cho đồ thị
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Dòng đầu tiên
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
        freq_slider = tk.Scale(band_frame, from_=from_, to=to_, orient="horizontal", label="Frequency", 
                            #    command=self.update_band_value
                               )
        freq_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        freq_slider.set(params['freq'])
        freq_slider.pack()

        # Tạo slider cho Q
        q_slider = tk.Scale(band_frame, from_=0.1, to=10, resolution=0.1, orient="horizontal", label="Q", 
                            # command=self.update_band_value
                            )
        q_slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_band_value(band))
        q_slider.set(params['Q'])
        q_slider.pack()

        # Tạo slider cho Gain
        gain_slider = tk.Scale(band_frame, from_=-24, to=24, orient="horizontal", label="Gain (dB)",
                            #    command=self.update_band_value
                               )
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
        # print("update_band_value")
        bands = {}
        for band_name, controls in self.band_controls.items():
            freq = controls['freq_slider'].get()
            Q = controls['q_slider'].get()
            gain = controls['gain_slider'].get()

            # self.view_model.bands[band_name] = {'freq': freq, 'Q': Q, 'gain': gain}
            bands[band_name] = {'freq': freq, 'Q': Q, 'gain': gain}
        self.bands = bands
        self.view_model.update_band_values(self.bands)
        
    def update_view(self, event_name, data):
        if event_name == "filter_coeff_changed":
            print("filter_coeff_changed", data)
            self.setup_axs()
            self.canvas.draw()

    def setup_axs(self):
        self.ax.clear()
        f, hs = self.view_model.get_frequency_response()
        for h in hs:
            self.ax.semilogx(f, 20 * np.log10(abs(h)))

        # Cài đặt tiêu đề và nhãn
        self.ax.set_title('Đáp ứng tần số - Các Bộ Lọc (Peaking, Shelving, Highpass, Lowpass)')
        self.ax.set_xlabel('Tần số (Hz)')
        self.ax.set_ylabel('Độ lớn (dB)')
        self.ax.grid(True)
        self.ax.set_ylim([-30, 30])  # Giới hạn trục y từ -30 dB đến 30 dB
        # self.ax.legend()

        # Thêm dấu mốc tần số
        xticks = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
        self.ax.set_xticks(xticks)
        self.ax.set_xticklabels(['20', '50', '100', '200', '500', '1k', '2k', '5k', '10k', '20k'])
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)