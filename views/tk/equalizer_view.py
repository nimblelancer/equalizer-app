import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from tkinter import Toplevel
from views.equalizer_view2 import EqualizerView2

class EqualizerView:
    def __init__(self, root, view_model):
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=BOTH, expand=True)
        
        self.eqapply_var = ttk.IntVar()
        self.eq_checkbox = ttk.Checkbutton(self.frame, text="Enable Equalizer", variable=self.eqapply_var, command=self.update_equalizer, bootstyle="primary")
        self.eq_checkbox.pack()
        
        self.lowcut_var = ttk.IntVar()
        self.lowcut_checkbox = ttk.Checkbutton(self.frame, text="Enable Low Cut", variable=self.lowcut_var, command=self.update_equalizer, bootstyle="success")
        self.lowcut_checkbox.pack()
        
        self.highcut_var = ttk.IntVar()
        self.highcut_checkbox = ttk.Checkbutton(self.frame, text="Enable High Cut", variable=self.highcut_var, command=self.update_equalizer, bootstyle="danger")
        self.highcut_checkbox.pack()
        
        self.more_button = ttk.Button(self.frame, text="Advance Settings", command=self.open_more, bootstyle="info")
        self.more_button.pack(pady=5)
        
        self.sliders = {}
        bands = ["Bass", "Mid-bass", "Midrange", "Upper Mid", "Treble"]
        for band in bands:
            self.create_slider(band, -24, 24)
        
        self.view_model = view_model
    
    def create_slider(self, label, min_val, max_val):
        frame = ttk.Frame(self.frame)
        frame.pack(pady=5)
        ttk.Label(frame, text=label).pack()
        slider = ttk.Scale(frame, from_=min_val, to=max_val, orient=HORIZONTAL, command=self.update_equalizer)
        slider.pack()
        self.sliders[label] = slider
    
    def update_equalizer(self, event=None):
        settings = {band: self.sliders[band].get() for band in self.sliders}
        self.view_model.update_equalizer_info(self.eqapply_var.get(), settings)
    
    def open_more(self):
        new_window = Toplevel(self.frame)
        new_window.title("EQ Setting")