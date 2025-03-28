from core.filter.filter_design_with_buter import FilterDesignWithButter
from core.filter.filter_design_self_implemented import FilterDesignSelfImplemented
from core.filter.liner_filter import LinerFilter

class FilterProvider:
    """Lớp quản lý việc cung cấp các bộ lọc khác nhau (LowPass, HighPass, Peak)."""
    
    def __init__(self, fs=44100):
        self.fs = fs
        self.designers = {
            "butter": FilterDesignWithButter(fs=self.fs),
            "custom": FilterDesignSelfImplemented(fs=self.fs)
        }

    def create_lowpass_filter(self, cutoff_freq, filter_design="butter"):
        if filter_design == "butter":
            b, a = self.designers["butter"].design_lowpass_filter(cutoff_freq, order=4)
        elif filter_design == "custom":
            b, a = self.designers["custom"].design_lowpass_filter(cutoff_freq)
        else:
            raise ValueError(f"Filter design {filter_design} không hợp lệ.")
        return LinerFilter(b, a)

    def create_highpass_filter(self, cutoff_freq, filter_design="butter"):
        """Tạo bộ lọc HighPass (Butterworth hoặc FIR)."""
        if filter_design == "butter":
            b, a = self.designers["butter"].design_highpass_filter(cutoff_freq, order=4)
        elif filter_design == "custom":
            b, a = self.designers["custom"].design_highpass_filter(cutoff_freq)
        else:
            raise ValueError(f"Filter design {filter_design} không hợp lệ.")
        return LinerFilter(b, a)

    def create_peak_filter(self, bands, filter_design="custom"):
        """Tạo bộ lọc Peaking Equalizer."""
        b, a = self.designers[filter_design].design_peaking_filter(bands)
        return LinerFilter(b, a)
    
    def create_notch_filter(self, freq, Q=30, filter_design="butter"):
        """Tạo bộ lọc Notch Equalizer."""
        b, a = self.designers[filter_design].design_notch_filter(freq, Q=Q)
        return LinerFilter(b, a)
    
    def create_bandstop_filter(self, lfreq, hfreq, filter_design="butter"):
        """Tạo bộ lọc Notch Equalizer."""
        b, a = self.designers[filter_design].design_bandstop_filter(lfreq, hfreq)
        return LinerFilter(b, a)
