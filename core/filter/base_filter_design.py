from abc import ABC, abstractmethod

class G2FilterDesign(ABC):
    def __init__(self, fs=44100):
        self.fs = fs

    @abstractmethod
    def design_lowpass_filter(self, fc, order=None):
        pass

    @abstractmethod
    def design_highpass_filter(self, fc, order=None):
        pass

    @abstractmethod
    def design_bandstop_filter(self, flow=None, fhigh=None, gain=1.0, order=4):
        pass

    @abstractmethod
    def design_notch_filter(self, fc=None, Q=30, order=4):
        pass