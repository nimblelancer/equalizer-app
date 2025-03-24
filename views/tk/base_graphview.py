import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.fft import fft
import scipy.signal as signal
import wave

class G2BaseGraphView:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(11.5, 4))

        self._plot_init()

        # self.ax.plot(xf, amplitude)
        self.ax.set_title("Frequency Spectrum")
        self.ax.set_xlabel("Frequency [Hz]")
        self.ax.set_ylabel("Amplitude")
        # return self.fig
    
    def _plot_init():
        # ax.plot(xf, amplitude)
    """"""