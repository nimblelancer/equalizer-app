import numpy as np
import math
from scipy.signal import butter
from core.filter.base_filter_design import G2FilterDesign

class FilterDesignWithButter(G2FilterDesign):
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
    
    