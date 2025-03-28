import numpy as np
import math
from scipy.signal import butter
from core.filter.base_filter_design import G2FilterDesign

class FilterDesignSelfImplemented(G2FilterDesign):
    def design_lowpass_filter(self, fc, order=None, Q=0.707):
        nyquist = 0.5 * self.fs
        fc_normalized = fc / nyquist
        if order is not None:
            return butter(order, fc_normalized, btype='low')
        else:
            order = np.ceil(np.log10(1 / (2 * Q)) / np.log10(fc_normalized))
            return butter(order, fc_normalized, btype='low')

    def design_highpass_filter(self, fc, order=None, Q=0.707):
        nyquist = 0.5 * self.fs
        fc_normalized = fc / nyquist
        if order is not None:
            return butter(order, fc_normalized, btype='high')
        else:
            order = np.ceil(np.log10(1 / (2 * Q)) / np.log10(fc_normalized))
            return butter(order, fc_normalized, btype='high')

    def design_bandpass_filter(self, f_center=None, fc_low=None, fc_high=None, gain=1.0, order=4, Q=0.707):
        if f_center is not None:
            fc_low = f_center / math.sqrt(Q)
            fc_high = f_center * math.sqrt(Q)

        nyquist = 0.5 * self.fs
        low = fc_low / nyquist
        high = fc_high / nyquist
        b, a = butter(order, [low, high], btype='band')
        
        if gain != 1.0:
            b = b * gain  # Adjust gain on the feedforward coefficients (b)
        
        return b, a

    def design_bandnotch_filter(self, f_center=None, fc_low=None, fc_high=None, order=4, Q=0.707):
        if f_center is not None:
            fc_low = f_center / math.sqrt(Q)
            fc_high = f_center * math.sqrt(Q)

        nyquist = 0.5 * self.fs
        low = fc_low / nyquist
        high = fc_high / nyquist
        return butter(order, [low, high], btype='bandstop')
    
    def design_peaking_filter(self, bands):
        """Tạo bộ lọc Peaking Equalizer cho các dải tần số."""
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