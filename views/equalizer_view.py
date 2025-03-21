import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.equalizer_advance_view import EqualizerAdvanceView


class EqualizerView(ttk.Labelframe):
    def __init__(self, master):
        super().__init__(master, text="Equalizer", padding=10)
        self.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

        self.columnconfigure(list(range(9)), weight=1)
        self.rowconfigure(2, weight=1)

        self.create_controls()
        self.create_equalizer_bands()
        self.create_additional_controls()
        btn = ttk.Button(self, text="Advanced Settings", bootstyle=LINK, command=self.open_advance_view)
        btn.grid(row=3, column=0, columnspan=5, pady=10)

    def create_controls(self):
        """Tạo phần điều khiển trên cùng"""
        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=0, columnspan=9, sticky="ew", pady=5)

        for i in range(5):
            control_frame.columnconfigure(i, weight=1)

        # Switch On/Off với trace
        self.eq_status = ttk.BooleanVar(value=True)
        self.eq_status.trace_add('write', lambda *args: self.toggle_equalizer())

        self.switch = ttk.Checkbutton(
            control_frame, variable=self.eq_status,
            text="On", bootstyle="round-toggle"
        )
        self.switch.grid(row=0, column=4, padx=5)

    def toggle_equalizer(self):
        """Bật/tắt Equalizer (mượt mà, đồng bộ hơn)"""
        status = self.eq_status.get()
        self.switch.configure(text="Equalizer: ON" if status else "Equalizer: OFF")
        # Optional: update UI hoặc disable các controls nếu cần

    def create_equalizer_bands(self):
        col = 0
        for band in ['Bass', 'Mid-bass', 'Midrange', 'Upper Mid', 'Treble']:
            self.create_band(band, col)
            col += 1
    
    def create_band(self, text, col):
        """Tạo band cho Equalizer"""
        min_gain = -12
        max_gain = 12
        value = 0  # Mặc định 0 dB
        var = ttk.StringVar(value=f"{value} dB")

        # Label cho tên band (Bass, Mid-bass, ...)
        ttk.Label(self, text=text, anchor=CENTER).grid(row=2, column=col, pady=(0, 5))

        # Frame chứa Scale + Label value
        band_frame = ttk.Frame(self)
        band_frame.grid(row=1, column=col, padx=5)

        # Hiển thị giá trị Gain hiện tại bên trái slider
        ttk.Label(band_frame, textvariable=var, width=5, anchor=CENTER).pack(side=LEFT)

        # Scale Gain (dB)
        scale = ttk.Scale(
            band_frame, orient=VERTICAL, from_=max_gain, to=min_gain, value=value,
            command=lambda val, v=var: v.set(f"{int(float(val))} dB"),
            bootstyle=INFO, length=120
        )
        scale.pack(side=LEFT)


    def create_additional_controls(self):
        """Thêm phần mới như trong ảnh (checkbox + slider ngang + radio button)"""
        additional_frame = ttk.Frame(self)
        additional_frame.grid(row=4, column=0, columnspan=9, sticky="ew", pady=10)

        # Checkbox
        self.low_cut_var = ttk.BooleanVar()
        self.high_cut_var = ttk.BooleanVar()
        self.notch_filter_var = ttk.BooleanVar()
        ttk.Checkbutton(additional_frame, text="Low Cut", variable=self.low_cut_var).grid(row=0, column=0, padx=5)
        ttk.Checkbutton(additional_frame, text="High Cut", variable=self.high_cut_var).grid(row=0, column=1, padx=5)
        ttk.Checkbutton(additional_frame, text="Notch Filter", variable=self.notch_filter_var).grid(row=0, column=2, padx=5)

        # Low Cut Slider
        ttk.Label(additional_frame, text="Low Cut (Hz)").grid(row=1, column=0, padx=5, sticky=E)
        self.low_cut_value = ttk.StringVar(value="20")
        low_cut_frame = ttk.Frame(additional_frame)
        low_cut_frame.grid(row=1, column=1, columnspan=2, sticky="ew")
        self.low_cut_slider = ttk.Scale(low_cut_frame, orient=HORIZONTAL, from_=20, to=200, length=150,
                                        command=lambda val: self.low_cut_value.set(f"{int(float(val))}"))
        self.low_cut_slider.pack(side=LEFT)
        ttk.Label(low_cut_frame, textvariable=self.low_cut_value).pack(side=LEFT, padx=5)

        # High Cut Slider
        ttk.Label(additional_frame, text="High Cut (kHz)").grid(row=2, column=0, padx=5, sticky=E)
        self.high_cut_value = ttk.StringVar(value="15")
        high_cut_frame = ttk.Frame(additional_frame)
        high_cut_frame.grid(row=2, column=1, columnspan=2, sticky="ew")
        self.high_cut_slider = ttk.Scale(high_cut_frame, orient=HORIZONTAL, from_=1, to=20, length=150,
                                        command=lambda val: self.high_cut_value.set(f"{int(float(val))}"))
        self.high_cut_slider.pack(side=LEFT)
        ttk.Label(high_cut_frame, textvariable=self.high_cut_value).pack(side=LEFT, padx=5)

        # Radio Button FIR/IIR
        ttk.Label(additional_frame, text="Filter Type").grid(row=3, column=0, padx=5, sticky=E)
        self.filter_var = ttk.StringVar(value="FIR")
        ttk.Radiobutton(additional_frame, text="FIR", variable=self.filter_var, value="FIR").grid(row=3, column=1, sticky=W)
        ttk.Radiobutton(additional_frame, text="IIR", variable=self.filter_var, value="IIR").grid(row=3, column=2, sticky=W)

    def open_advance_view(self):
        EqualizerAdvanceView(self)

    def update_value(self, value, name):
        """Cập nhật giá trị khi thanh trượt thay đổi"""
        self.setvar(name, f"{float(value):.0f}")

    def toggle_equalizer(self):
        """Bật/tắt Equalizer"""
        status = "On" if self.eq_status.get() else "Off"
        self.switch.configure(text=status)
