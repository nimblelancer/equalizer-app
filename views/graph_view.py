import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphView(tk.LabelFrame):
    def __init__(self, parent, style):
        self.style = style
        super().__init__(parent, text="Audio Analysis Graphs")
        self.theme_bg = self.get_theme_background()
        self.theme_fg = self.get_theme_foreground()
        
        # Tạo Figure chứa biểu đồ
        self.fig = Figure(figsize=(5, 5), dpi=100, facecolor=self.theme_bg)
        self.fig.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.08)
        self.fig.subplots_adjust(hspace=0.3, wspace=0.3)

        # Tạo 6 Subplots (3 hàng, 2 cột)
        # Hàng 1: Frequency Response
        self.ax_resp_orig = self.fig.add_subplot(321)
        self.set_ax_style(self.ax_resp_orig, "Original Response")
        
        self.ax_resp_eq = self.fig.add_subplot(322)
        self.set_ax_style(self.ax_resp_eq, "Equalized Response")
        
        # Hàng 2: Frequency Spectrum
        self.ax_spec_orig = self.fig.add_subplot(323)
        self.set_ax_style(self.ax_spec_orig, "Spectrum - Original")
        
        self.ax_spec_eq = self.fig.add_subplot(324)
        self.set_ax_style(self.ax_spec_eq, "Spectrum - Equalized")
        
        # Hàng 3: Waveform
        self.ax_wave_orig = self.fig.add_subplot(325)
        self.set_ax_style(self.ax_wave_orig, "Waveform - Original")
        
        self.ax_wave_eq = self.fig.add_subplot(326)
        self.set_ax_style(self.ax_wave_eq, "Waveform - Equalized")

        # Tạo dữ liệu giả lập cho tất cả các biểu đồ
        self.init_data()
        
        # Nhúng Figure vào Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        
        # Cấu hình layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Vẽ tất cả các biểu đồ
        self.plot_all_graphs()

    def init_data(self):
        """Khởi tạo tất cả dữ liệu cho các biểu đồ"""
        # Dữ liệu cho Frequency Response
        self.freqs_resp = np.logspace(1, 4, 100)
        self.original_amplitude = np.sin(np.log10(self.freqs_resp)) * 10
        self.equalized_amplitude = self.original_amplitude.copy()
        
        # Dữ liệu cho Frequency Spectrum
        self.freqs_spec = np.logspace(1, 4, 200)
        self.original_spectrum = np.abs(np.sin(np.log10(self.freqs_spec)) * 300)
        self.equalized_spectrum = self.original_spectrum * np.random.uniform(0.8, 1.2, len(self.freqs_spec))
        
        # Dữ liệu cho Waveform
        self.time = np.linspace(0, 5000, 5000)
        self.original_waveform = np.random.normal(0, 0.5, 5000)
        self.equalized_waveform = np.sign(np.random.normal(0, 1, 5000))

    def plot_all_graphs(self):
        """Vẽ tất cả các biểu đồ"""
        # Vẽ Frequency Response
        self.ax_resp_orig.plot(self.freqs_resp, self.original_amplitude, label="Original", color="blue")
        self.ax_resp_eq.plot(self.freqs_resp, self.equalized_amplitude, label="Equalized", color="red")
        
        # Vẽ Frequency Spectrum
        self.ax_spec_orig.plot(self.freqs_spec, self.original_spectrum, label="Original", color="blue")
        self.ax_spec_eq.plot(self.freqs_spec, self.equalized_spectrum, label="Equalized", color="brown")
        self.ax_spec_orig.set_xscale("log")
        self.ax_spec_eq.set_xscale("log")
        
        # Vẽ Waveform
        self.ax_wave_orig.plot(self.time, self.original_waveform, label="Original", color="blue")
        self.ax_wave_eq.plot(self.time, self.equalized_waveform, label="Equalized", color="red")
        
        # Thêm legend cho tất cả các biểu đồ
        for ax in [self.ax_resp_orig, self.ax_resp_eq, self.ax_spec_orig, 
                  self.ax_spec_eq, self.ax_wave_orig, self.ax_wave_eq]:
            ax.legend(loc="upper right")
        
        # Cập nhật canvas
        self.canvas.draw()

    def update_frequency_response(self, new_equalized_amplitude=None):
        """Cập nhật biểu đồ Frequency Response"""
        if new_equalized_amplitude is None:
            self.equalized_amplitude = self.original_amplitude + np.random.uniform(-3, 3, len(self.freqs_resp))
        else:
            self.equalized_amplitude = new_equalized_amplitude
            
        self.ax_resp_eq.clear()
        self.set_ax_style(self.ax_resp_eq, "Equalized Response")
        self.ax_resp_eq.plot(self.freqs_resp, self.equalized_amplitude, label="Equalized", color="red")
        self.ax_resp_eq.legend(loc="upper right")
        self.canvas.draw()

    def update_spectrum(self, new_equalized_spectrum=None):
        """Cập nhật biểu đồ Frequency Spectrum"""
        if new_equalized_spectrum is None:
            self.equalized_spectrum = self.original_spectrum * np.random.uniform(0.8, 1.2, len(self.freqs_spec))
        else:
            self.equalized_spectrum = new_equalized_spectrum
            
        self.ax_spec_eq.clear()
        self.set_ax_style(self.ax_spec_eq, "Spectrum - Equalized")
        self.ax_spec_eq.plot(self.freqs_spec, self.equalized_spectrum, label="Equalized", color="brown")
        self.ax_spec_eq.set_xscale("log")
        self.ax_spec_eq.legend(loc="upper right")
        self.canvas.draw()

    def update_waveform(self, new_equalized_waveform=None):
        """Cập nhật biểu đồ Waveform"""
        if new_equalized_waveform is None:
            self.equalized_waveform = np.sign(np.random.normal(0, 1, 5000))
        else:
            self.equalized_waveform = new_equalized_waveform
            
        self.ax_wave_eq.clear()
        self.set_ax_style(self.ax_wave_eq, "Waveform - Equalized")
        self.ax_wave_eq.plot(self.time, self.equalized_waveform, label="Equalized", color="red")
        self.ax_wave_eq.legend(loc="upper right")
        self.canvas.draw()

    def update_all_graphs(self):
        """Cập nhật tất cả các biểu đồ"""
        self.update_frequency_response()
        self.update_spectrum()
        self.update_waveform()

    def set_ax_style(self, ax, title):
        """Định dạng màu chữ và màu nền cho từng subplot"""
        ax.set_facecolor(self.theme_bg)
        ax.set_title(title, color=self.theme_fg)
        
        # Thêm nhãn phù hợp dựa trên loại biểu đồ
        if "Response" in title:
            ax.set_xlabel("Frequency (Hz)", color=self.theme_fg)
            ax.set_ylabel("Amplitude (dB)", color=self.theme_fg)
        elif "Spectrum" in title:
            ax.set_xlabel("Frequency (Hz)", color=self.theme_fg)
            ax.set_ylabel("Amplitude", color=self.theme_fg)
        elif "Waveform" in title:
            ax.set_xlabel("Time (ms)", color=self.theme_fg)
            ax.set_ylabel("Amplitude", color=self.theme_fg)
        
        # Cập nhật màu chữ cho trục x và y
        ax.tick_params(axis='x', colors=self.theme_fg)
        ax.tick_params(axis='y', colors=self.theme_fg)
        
        # Cập nhật màu viền
        for spine in ax.spines.values():
            spine.set_color(self.theme_fg)

    def get_theme_background(self):
        """Lấy màu nền từ theme hiện tại của ttkbootstrap"""
        return self.style.lookup("TLabel", "background")
    
    def get_theme_foreground(self):
        """Lấy màu chữ từ theme hiện tại của ttkbootstrap"""
        return self.style.lookup("TLabel", "foreground")