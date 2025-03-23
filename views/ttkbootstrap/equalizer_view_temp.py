import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from tkinter import Toplevel
from views.equalizer_view2 import EqualizerView2

class EqualizerView(ttk.Frame):
    def __init__(self, root, view_model):
        super().__init__(root)
        self.view_model = view_model
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Khung chứa Equalizer
        self.frame = ttk.Labelframe(self, text="🎚️ Equalizer", padding=10, bootstyle="primary")
        self.frame.pack(fill=BOTH, expand=True)

        # Checkbox bật/tắt Equalizer
        self.eqapply_var = ttk.IntVar()
        self.eq_checkbox = ttk.Checkbutton(self.frame, text="Enable Equalizer", variable=self.eqapply_var, command=self.update_equalizer)
        self.eq_checkbox.grid(row=0, column=0, columnspan=2, pady=5, sticky=W)

        # Checkbox Low Cut & High Cut
        self.lowcut_var = ttk.IntVar()
        self.lowcut_checkbox = ttk.Checkbutton(self.frame, text="Enable Low Cut", variable=self.lowcut_var, command=self.update_equalizer)
        self.lowcut_checkbox.grid(row=1, column=0, pady=5, sticky=W)

        self.highcut_var = ttk.IntVar()
        self.highcut_checkbox = ttk.Checkbutton(self.frame, text="Enable High Cut", variable=self.highcut_var, command=self.update_equalizer)
        self.highcut_checkbox.grid(row=1, column=1, pady=5, sticky=W)

        # Nút mở cài đặt nâng cao
        self.more_button = ttk.Button(self.frame, text="⚙️ Advance Settings", command=self.open_more)
        self.more_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Thanh chỉnh Equalizer
        self.sliders = {}
        bands = ["Bass", "Mid-bass", "Midrange", "Upper Mid", "Treble"]
        for i, band in enumerate(bands):
            self.create_slider(band, -24, 24, i+3)

    def create_slider(self, label, min_val, max_val, row):
        ttk.Label(self.frame, text=label).grid(row=row, column=0, pady=5)
        slider = ttk.Scale(self.frame, from_=min_val, to=max_val, orient=HORIZONTAL, command=self.update_equalizer)
        slider.grid(row=row, column=1, padx=5, pady=5, sticky=EW)
        self.sliders[label] = slider

    def update_equalizer(self, event=None):
        settings = {band: self.sliders[band].get() for band in self.sliders}
        self.view_model.update_equalizer_info(self.eqapply_var.get(), settings)

    def open_more(self):
        new_window = Toplevel(self.frame)
        new_window.title("EQ Setting")
     