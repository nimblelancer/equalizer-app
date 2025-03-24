import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

class AudioSpectrumGraphView:
    def __init__(self, parent, framerate=44100, buffer_size=1024*10):
        self.canvas_frame = tk.Frame(parent)
        self.canvas_frame.pack()
        self.canvas = None
        self.g1 = None  # Đồ thị biên độ theo thời gian
        self.g2 = None  # Đồ thị phổ tần số của dữ liệu âm thanh
        self.g3 = None  # Đồ thị phổ tần số của dữ liệu đã lọc
        self.framerate = framerate
        self.buffer_size = buffer_size

    # def show_graph(self):
        # Tạo đồ thị nếu chưa tạo
        if self.canvas is None:
            fig, axs = plt.subplots(2, 1, figsize=(10, 9))

            # Tạo đồ thị biên độ theo thời gian (g1)
            self.g1, = axs[0].plot([], [], label='Audio Signal', color='b')
            axs[0].set_xlim(0, self.buffer_size)
            axs[0].set_ylim(-1, 1)
            axs[0].set_title("Audio Signal - Time Domain")
            axs[0].set_xlabel("Samples")
            axs[0].set_ylabel("Amplitude")

            # Tạo đồ thị phổ tần số (g2 cho audio_data và g3 cho filtered_data)
            self.g2, = axs[1].plot([], [], label='Audio Signal Spectrum', color='b')
            self.g3, = axs[1].plot([], [], label='Filtered Signal Spectrum', color='r')
            axs[1].set_xlim(0, self.framerate // 2)  # Xem phổ tần số từ 0 đến Nyquist frequency
            axs[1].set_ylim(0, 1)  # Quy mô phổ tần số
            axs[1].set_title("Frequency Spectrum")
            axs[1].set_xlabel("Frequency (Hz)")
            axs[1].set_ylabel("Magnitude")
            axs[1].legend()

            # Đặt đồ thị vào Tkinter canvas
            self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

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
