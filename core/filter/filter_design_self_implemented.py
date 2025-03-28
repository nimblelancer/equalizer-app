import numpy as np
import math
from scipy.signal import butter
from core.filter.base_filter_design import G2FilterDesign

class FilterDesignSelfImplemented(G2FilterDesign):
    def design_lowpass_filter(self, fc, fs=44100, order=4):
        nyquist = 0.5 * fs
        fc_normalized = fc / nyquist
        return butter(order, fc_normalized, btype='low')

    def design_highpass_filter(self, fc, fs=44100, order=4):
        
        nyquist = 0.5 * fs
        fc_normalized = fc / nyquist
        return butter(order, fc_normalized, btype='high')

    def design_bandstop_filter(self, fc_low=None, fc_high=None, fs=44100, order=4):
        nyquist = 0.5 * fs
        low = fc_low / nyquist
        high = fc_high / nyquist
        return butter(order, [low, high], btype='bandstop')
    
    def design_notch_filter(self, fc, fs=44100, Q=30, order=4):
        nyquist = 0.5 * fs
        # Tính dải băng (bandwidth) từ Q
        bandwidth = fc / Q
        # Tính tần số cắt thấp và cao của bộ lọc notch
        f1_normalized = (fc - bandwidth / 2) / nyquist
        f2_normalized = (fc + bandwidth / 2) / nyquist
        # Tạo bộ lọc bandstop (notch)
        return butter(order, [f1_normalized, f2_normalized], btype='bandstop')
    
    def design_peaking_filter(self, bands):
        b_total_peak = np.array([1])
        a_total_peak = np.array([1])

        for band_name, params in bands.items():
            f0 = params['freq']
            Q = params['Q']
            gain = params['gain']

            # Tạo bộ lọc Peaking và cộng dồn
            b, a = self.peaking_filter(f0, Q, gain)
            b_total_peak = np.convolve(b_total_peak, b)
            a_total_peak = np.convolve(a_total_peak, a)

        return b_total_peak, a_total_peak

    def peaking_filter(self, f0, Q, gain):
        omega0 = 2 * np.pi * f0 / self.fs  # Tần số góc trung tâm
        alpha = np.sin(omega0) / (2 * Q)

        A = 10 ** (gain / 40)  # Độ khuếch đại

        b0 = 1 + alpha * A
        b1 = -2 * np.cos(omega0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(omega0)
        a2 = 1 - alpha / A

        b = np.array([b0, b1, b2]) / a0
        a = np.array([a0, a1, a2]) / a0
        return b, a