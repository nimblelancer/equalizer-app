from abc import ABC, abstractmethod

class G2FilterDesign(ABC):
    def __init__(self, fs=44100):
        self.fs = fs

    @abstractmethod
    def design_lowpass_filter(self, fc, order=None, Q=0.707):
        pass

    @abstractmethod
    def design_highpass_filter(self, fc, order=None, Q=0.707):
        pass

    @abstractmethod
    def design_bandpass_filter(self, f_center=None, fc_low=None, fc_high=None, gain=1.0, order=4, Q=0.707):
        pass

    @abstractmethod
    def design_bandnotch_filter(self, f_center=None, fc_low=None, fc_high=None, order=4, Q=0.707):
        pass