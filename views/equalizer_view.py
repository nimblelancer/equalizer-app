import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.equalizer_advance_view import EqualizerAdvanceView


class EqualizerView(ttk.Labelframe):
    def __init__(self, master):
        super().__init__(master, text="Equalizer", padding=5)
        self.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.columnconfigure(list(range(6)), weight=1)

        self.create_header()
        self.create_equalizer_bands()
        self.create_additional_controls()
        btn = ttk.Button(self, text="Advanced Settings", bootstyle=LINK, command=self.open_advance_view)
        btn.grid(row=6, column=0, columnspan=6, pady=(15, 0))

    def create_header(self):
        header_frame = ttk.Frame(self)
        header_frame.grid(row=0, column=0, columnspan=6, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=0)

        
        self.eq_status = ttk.BooleanVar(value=True)
        self.switch = ttk.Checkbutton(header_frame, variable=self.eq_status,
                                      text="On", bootstyle="round-toggle")
        self.switch.grid(row=0, column=1, sticky=E, padx=5)

    def create_equalizer_bands(self):
        for col, band in enumerate(['Bass', 'Mid-bass', 'Midrange', 'Upper Mid', 'Treble']):
            self.create_band(band, col)

    def create_band(self, text, col):
        min_gain = -12
        max_gain = 12
        value = 0
        var = ttk.StringVar(value=f"{value} dB")

        ttk.Label(self, text=text, anchor=CENTER).grid(row=1, column=col, pady=(5, 0))
        band_frame = ttk.Frame(self)
        band_frame.grid(row=2, column=col, padx=10)
        ttk.Label(band_frame, textvariable=var, width=6, anchor=CENTER).pack(side=TOP, pady=(0, 5))
        scale = ttk.Scale(
            band_frame, orient=VERTICAL, from_=max_gain, to=min_gain, value=value,
            command=lambda val, v=var: v.set(f"{int(float(val))} dB"),
            bootstyle=INFO, length=140
        )
        scale.pack()

    def create_additional_controls(self):
        additional_frame = ttk.Frame(self)
        additional_frame.grid(row=3, column=0, columnspan=6, sticky="ew", pady=(20, 10))
        additional_frame.columnconfigure(list(range(6)), weight=1)

        # Checkbox hàng 1
        ttk.Checkbutton(additional_frame, text="Low Cut", variable=ttk.BooleanVar()).grid(row=0, column=0, padx=10, sticky=W)
        ttk.Checkbutton(additional_frame, text="High Cut", variable=ttk.BooleanVar()).grid(row=0, column=1, padx=10, sticky=W)
        ttk.Checkbutton(additional_frame, text="Notch Filter", variable=ttk.BooleanVar()).grid(row=0, column=2, padx=10, sticky=W)

        # Slider Low Cut
        ttk.Label(additional_frame, text="Low Cut (Hz)").grid(row=1, column=0, padx=5, sticky=E, pady=(10, 0))
        self.low_cut_value = ttk.StringVar(value="20")
        low_cut_slider = ttk.Scale(additional_frame, orient=HORIZONTAL, from_=20, to=200, length=150,
                                   command=lambda val: self.low_cut_value.set(f"{int(float(val))}"))
        low_cut_slider.grid(row=1, column=1, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Label(additional_frame, textvariable=self.low_cut_value).grid(row=1, column=3, sticky=W, pady=(10, 0))

        # Slider High Cut
        ttk.Label(additional_frame, text="High Cut (kHz)").grid(row=2, column=0, padx=5, sticky=E, pady=(10, 0))
        self.high_cut_value = ttk.StringVar(value="15")
        high_cut_slider = ttk.Scale(additional_frame, orient=HORIZONTAL, from_=1, to=20, length=150,
                                    command=lambda val: self.high_cut_value.set(f"{int(float(val))}"))
        high_cut_slider.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Label(additional_frame, textvariable=self.high_cut_value).grid(row=2, column=3, sticky=W, pady=(10, 0))

        # Radio
        ttk.Label(additional_frame, text="Filter Type").grid(row=3, column=0, padx=5, sticky=E, pady=(10, 0))
        self.filter_var = ttk.StringVar(value="FIR")
        ttk.Radiobutton(additional_frame, text="FIR", variable=self.filter_var, value="FIR").grid(row=3, column=1, sticky=W, pady=(10, 0))
        ttk.Radiobutton(additional_frame, text="IIR", variable=self.filter_var, value="IIR").grid(row=3, column=2, sticky=W, pady=(10, 0))

    def open_advance_view(self):
        EqualizerAdvanceView(self)
