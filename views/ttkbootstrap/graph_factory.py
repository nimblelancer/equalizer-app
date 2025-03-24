import numpy as np


class GraphFactory:
    def __init__(self, ax):
        self.ax = ax
        self.line = None
        self.im = None

    def create_waveform(self):
        """
        Khởi tạo đồ thị Waveform mà không có dữ liệu.
        """
        self.line, = self.ax.plot([], [])
        self.ax.set_title("Waveform")
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel("Amplitude")

    def create_spectrogram(self):
        """
        Khởi tạo Spectrogram mà không có dữ liệu.
        """
        self.im = self.ax.imshow(np.zeros((1, 1)), aspect="auto", origin="lower", cmap="viridis")
        self.ax.set_title("Spectrogram")
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel("Frequency [Hz]")

    def create_frequency_spectrum(self):
        """
        Khởi tạo Frequency Spectrum mà không có dữ liệu.
        """
        self.line, = self.ax.plot([], [])
        self.ax.set_title("Frequency Spectrum")
        self.ax.set_xlabel("Frequency [Hz]")
        self.ax.set_ylabel("Amplitude")

    def create_volume_level(self):
        """
        Khởi tạo Volume Level mà không có dữ liệu.
        """
        self.line, = self.ax.plot([], [])
        self.ax.set_title("Volume Level")
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel("Amplitude")

    def create_bar_chart(self):
        """
        Khởi tạo Bar Chart mà không có dữ liệu.
        """
        self.bar = self.ax.bar(['bass', 'mid_bass', 'midrange', 'upper_mid', 'treble'], [0,0,0,0,0], color=['blue', 'green', 'orange', 'red', 'purple'])
        self.ax.set_title("Bar Chart")
        self.ax.set_xlabel("Frequency Bands")
        self.ax.set_ylabel("Amplitude")

    def create_fft(self):
        """
        Khởi tạo FFT mà không có dữ liệu.
        """
        self.line, = self.ax.plot([], [])
        self.ax.set_title("FFT")
        self.ax.set_xlabel("Frequency [Hz]")
        self.ax.set_ylabel("Log(Amplitude)")

    def create_frequency_response(self):
        """
        Khởi tạo Frequency Response mà không có dữ liệu.
        """
        self.line, = self.ax.plot([], [])
        self.ax.set_title("Frequency Response")
        self.ax.set_xscale('log')
        self.ax.set_xlabel("Frequency [Hz]")
        self.ax.set_ylabel("Magnitude")