import numpy as np
import math
from scipy.signal import butter
from core.filter.base_filter_design import G2FilterDesign

class FilterDesignWithButter(G2FilterDesign):
    def design_lowpass_filter(self, fc, fs=44100, order=None, Q=0.707):
        nyquist = 0.5 * fs
        fc_normalized = fc / nyquist
        if order is not None:
            return butter(order, fc_normalized, btype='low')
        else:
            order = np.ceil(np.log10(1 / (2 * Q)) / np.log10(fc_normalized))
            return butter(order, fc_normalized, btype='low')

    def design_highpass_filter(self, fc, fs=44100, order=None, Q=0.707):
        
        nyquist = 0.5 * fs
        fc_normalized = fc / nyquist
        
        if order is not None:
            return butter(order, fc_normalized, btype='high')
        else:
            order = np.ceil(np.log10(1 / (2 * Q)) / np.log10(fc_normalized))
            return butter(order, fc_normalized, btype='high')

    def design_bandpass_filter(self, f_center=None, fc_low=None, fc_high=None, fs=44100, gain=1.0, order=4, Q=0.707):
        if f_center is not None:
            fc_low = f_center / math.sqrt(Q)
            fc_high = f_center * math.sqrt(Q)

        nyquist = 0.5 * fs
        low = fc_low / nyquist
        high = fc_high / nyquist
        b, a = butter(order, [low, high], btype='band')
        
        if gain != 1.0:
            b = b * gain  # Adjust gain on the feedforward coefficients (b)
        
        return b, a

    def design_bandnotch_filter(self, f_center=None, fc_low=None, fc_high=None, fs=44100, order=4, Q=0.707):
        if f_center is not None:
            fc_low = f_center / math.sqrt(Q)
            fc_high = f_center * math.sqrt(Q)

        nyquist = 0.5 * fs
        low = fc_low / nyquist
        high = fc_high / nyquist
        return butter(order, [low, high], btype='bandstop')