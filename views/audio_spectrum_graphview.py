import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

class AudioSpectrumGraphView:
    def __init__(self, parent, framerate=44100, buffer_size=1024*10, theme_colors=None):
        self.theme_colors = theme_colors or {}
        self.canvas_frame = ttk.Frame(parent, padding=10)
        self.canvas_frame.pack(fill=BOTH, expand=YES)
        self.canvas = None
        self.g1 = None
        self.g2 = None
        self.g3 = None
        self.framerate = framerate
        self.buffer_size = buffer_size

    def show_graph(self):
        if self.canvas is None:
            fig_bg = self.theme_colors.get("bg", "#2e2e2e")
            fg_color = self.theme_colors.get("fg", "white")

            fig, axs = plt.subplots(2, 1, figsize=(10, 9), facecolor=fig_bg)

            # Tăng khoảng cách giữa 2 biểu đồ
            fig.subplots_adjust(hspace=0.5) # Đơn vị là độ

            for ax in axs:
                ax.set_facecolor(fig_bg)
                ax.title.set_color(fg_color)
                ax.xaxis.label.set_color(fg_color)
                ax.yaxis.label.set_color(fg_color)
                ax.tick_params(axis='x', colors=fg_color)
                ax.tick_params(axis='y', colors=fg_color)
                ax.spines['bottom'].set_color(fg_color)
                ax.spines['top'].set_color(fg_color)
                ax.spines['left'].set_color(fg_color)
                ax.spines['right'].set_color(fg_color)

            self.g1, = axs[0].plot([], [], label='Audio Signal', color=self.theme_colors.get("line1", "#00BFFF"))
            axs[0].set_xlim(0, self.buffer_size)
            axs[0].set_ylim(-1, 1)
            axs[0].set_title("Audio Signal - Time Domain", size=15)
            axs[0].set_xlabel("Samples")
            axs[0].set_ylabel("Amplitude")

            self.g2, = axs[1].plot([], [], label='Audio Signal Spectrum', color=self.theme_colors.get("line1", "#00BFFF"))
            self.g3, = axs[1].plot([], [], label='Filtered Signal Spectrum', color=self.theme_colors.get("line2", "#FF4500"))
            axs[1].set_xlim(0, self.framerate // 2)
            axs[1].set_ylim(0, 1)
            axs[1].set_title("Frequency Spectrum", size=15)
            axs[1].set_xlabel("Frequency (Hz)")
            axs[1].set_ylabel("Magnitude")
            axs[1].legend(facecolor=fig_bg, edgecolor=fg_color, labelcolor=fg_color)

            self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES)



    def plot_spectrum(self, audio_data, filtered_data):
        """Vẽ đồ thị phổ tần số của dữ liệu âm thanh và đã lọc"""
        if self.g1 is None or self.g2 is None or self.g3 is None:
            print("Error: One of the plot objects (g1, g2, g3) is None, make sure show_graph is called first.")
            return

        if self.canvas is None:
            print("Error: canvas is None, make sure show_graph is called first.")
            return

        # Cập nhật đồ thị biên độ theo thời gian (g1)
        self.g1.set_ydata(audio_data)  # Cập nhật dữ liệu biên độ theo thời gian
        self.g1.set_xdata(np.arange(len(audio_data)))  # Cập nhật trục x

        # Tính toán FFT của audio_data và filtered_data
        N = len(audio_data)
        freqs = fftfreq(N, d=1 / self.framerate)[:N // 2]  # Chỉ lấy phần dương của phổ tần số
        audio_fft = np.abs(fft(audio_data))[:N // 2]
        filtered_fft = np.abs(fft(filtered_data))[:N // 2]

        # Cập nhật đồ thị phổ tần số (g2 cho audio_data và g3 cho filtered_data)
        self.g2.set_xdata(freqs)
        self.g2.set_ydata(audio_fft)  # Cập nhật phổ tần số của audio_data

        self.g3.set_xdata(freqs)
        self.g3.set_ydata(filtered_fft)  # Cập nhật phổ tần số của filtered_data

        # Cập nhật đồ thị
        self.canvas.draw()

