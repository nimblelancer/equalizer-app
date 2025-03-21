import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import randint


class EqualizerView(ttk.Labelframe):
    def __init__(self, master):
        super().__init__(master, text="Equalizer", padding=10)
        self.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

        self.columnconfigure(list(range(9)), weight=1)
        self.rowconfigure(2, weight=1)

        self.create_controls()
        self.create_equalizer_bands()

    def create_controls(self):
        """Tạo phần điều khiển trên cùng"""
        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=0, columnspan=9, sticky="ew", pady=5)

        for i in range(5):
            control_frame.columnconfigure(i, weight=1)  # Căn chỉnh độ rộng

        # Preset
        ttk.Label(control_frame, text="Preset", anchor=E, width=8).grid(row=0, column=0, padx=5)
        self.preset_var = ttk.StringVar(value="Custom")
        ttk.Combobox(control_frame, textvariable=self.preset_var, values=["Custom", "Rock", "Pop", "Jazz"],
                     state="readonly", width=8).grid(row=0, column=1, padx=5)

        # Chọn thuật toán
        ttk.Label(control_frame, text="Algorithm", anchor=E, width=8).grid(row=0, column=2, padx=5)
        self.algorithm_var = ttk.StringVar(value="FIR")
        ttk.Combobox(control_frame, textvariable=self.algorithm_var, values=["IIR", "FIR", "FFT"],
                     state="readonly", width=8).grid(row=0, column=3, padx=5)

        # Switch On/Off
        self.eq_status = ttk.BooleanVar(value=True)
        self.switch = ttk.Checkbutton(control_frame, variable=self.eq_status, text="On",
                                      bootstyle="round-toggle", command=self.toggle_equalizer)
        self.switch.grid(row=0, column=4, padx=5)

    def create_equalizer_bands(self):
        """Tạo các dải tần số equalizer"""
        controls = ["62 Hz", "125 Hz", "250 Hz", "500 Hz", "1 kHz", "2 kHz", "4 kHz", "8 kHz", "16 kHz"]

        for col, control in enumerate(controls):
            self.create_band(control, col)

    def create_band(self, text, col):
        """Tạo một dải Equalizer"""
        value = randint(1, 99)
        var_name = f"var_{text}"
        self.setvar(var_name, value)

        
        ttk.Label(self, text=text, anchor=CENTER).grid(row=1, column=col, pady=5)

        
        scale = ttk.Scale(
            self, orient=VERTICAL, from_=99, to=1, value=value,
            command=lambda val, name=var_name: self.update_value(val, name),
            bootstyle=INFO, length=200
        )
        scale.grid(row=2, column=col, sticky="ns", padx=5, pady=5)

        # Giá trị hiển thị
        ttk.Label(self, textvariable=self.getvar(var_name)).grid(row=3, column=col, pady=5)

    def update_value(self, value, name):
        """Cập nhật giá trị khi thanh trượt thay đổi"""
        self.setvar(name, f"{float(value):.0f}")

    def toggle_equalizer(self):
        """Bật/tắt Equalizer"""
        status = "On" if self.eq_status.get() else "Off"
        self.switch.configure(text=status)


