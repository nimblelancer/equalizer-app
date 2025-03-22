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
        
        # Dynamically get screen width & height to adjust figsize
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        # Điều chỉnh theo cả width và height
        if screen_width < 1300 or screen_height < 700:  # Màn nhỏ
            print("Small screen detected")
            figsize = (2, 2)
            self.title_size = 7
            self.label_size = 6
            self.tick_size = 5
            hspace = 0.5
            wspace = 0.4
        elif screen_width < 1700 or screen_height < 900:  # Màn trung bình
            print("Medium screen detected")
            figsize = (4, 4)
            self.title_size = 9
            self.label_size = 8
            self.tick_size = 7
            hspace = 0.4
            wspace = 0.3
        else:  # Màn lớn
            print("Large screen detected")
            figsize = (4, 4)
            self.title_size = 8
            self.label_size = 7
            self.tick_size = 6
            hspace = 0.4
            wspace = 0.3
        
        # Figure
        self.fig = Figure(figsize=figsize, dpi=100, facecolor=self.theme_bg)
        self.fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08)
        self.fig.subplots_adjust(hspace=hspace, wspace=wspace)

        # 6 Subplots
        self.ax_resp_orig = self.fig.add_subplot(321)
        self.set_ax_style(self.ax_resp_orig, "Original Response")
        
        self.ax_resp_eq = self.fig.add_subplot(322)
        self.set_ax_style(self.ax_resp_eq, "Equalized Response")
        
        self.ax_spec_orig = self.fig.add_subplot(323)
        self.set_ax_style(self.ax_spec_orig, "Spectrum - Original")
        
        self.ax_spec_eq = self.fig.add_subplot(324)
        self.set_ax_style(self.ax_spec_eq, "Spectrum - Equalized")
        
        self.ax_wave_orig = self.fig.add_subplot(325)
        self.set_ax_style(self.ax_wave_orig, "Waveform - Original")
        
        self.ax_wave_eq = self.fig.add_subplot(326)
        self.set_ax_style(self.ax_wave_eq, "Waveform - Equalized")

        # Dummy data & Canvas
        self.init_data()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
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
        ax.set_facecolor(self.theme_bg)
        ax.set_title(title, color=self.theme_fg, size=self.title_size, loc='left')
        
        # Labels
        if "Response" in title:
            ax.set_xlabel("Frequency (Hz)", color=self.theme_fg, size=self.label_size)
            ax.set_ylabel("Amplitude (dB)", color=self.theme_fg, size=self.label_size)
        elif "Spectrum" in title:
            ax.set_xlabel("Frequency (Hz)", color=self.theme_fg, size=self.label_size)
            ax.set_ylabel("Amplitude", color=self.theme_fg, size=self.label_size)
        elif "Waveform" in title:
            ax.set_xlabel("Time (ms)", color=self.theme_fg, size=self.label_size)
            ax.set_ylabel("Amplitude", color=self.theme_fg, size=self.label_size)
        
        # Ticks
        ax.tick_params(axis='x', colors=self.theme_fg, labelsize=self.tick_size)
        ax.tick_params(axis='y', colors=self.theme_fg, labelsize=self.tick_size)
    
        for spine in ax.spines.values():
            spine.set_color(self.theme_fg)


    def get_theme_background(self):
        """Lấy màu nền từ theme hiện tại của ttkbootstrap"""
        return self.style.lookup("TLabel", "background")
    
    def get_theme_foreground(self):
        """Lấy màu chữ từ theme hiện tại của ttkbootstrap"""
        return self.style.lookup("TLabel", "foreground")