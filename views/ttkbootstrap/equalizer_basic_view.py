import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from viewmodels.equalizer_basic_viewmodel import EqualizerBasicViewModel

class EqualizerBasicView:
    def __init__(self, root, view_model: EqualizerBasicViewModel):
        self.frame = ttk.Frame(root)
        self.frame.grid(sticky="nsew")

        self.view_model = view_model
        
        self.sliders = {}
        self.band_labels = {}
        
        self.first_row_frame = ttk.Frame(self.frame)
        self.first_row_frame.grid(row=0, column=0, sticky="nsew")

        self.turnon_frame = ttk.Frame(self.first_row_frame)
        self.turnon_frame.grid(row=0, column=0, padx=5, sticky="n")

        # Enable Equalizer
        self.eqapply_var = ttk.IntVar(value=self.view_model.eq_apply)
        self.eq_checkbox = ttk.Checkbutton(
            self.turnon_frame, 
            text="Enable Equalizer", 
            variable=self.eqapply_var, 
            command=self.update_equalizer,
            bootstyle="success"
        )
        self.eq_checkbox.grid(row=0, column=0, sticky="w", pady=2)

        # Enable Low Cut
        self.lowcut_var = ttk.IntVar(value=self.view_model.lowcut_apply)
        self.lowcut_checkbox = ttk.Checkbutton(
            self.turnon_frame, 
            text="Enable Low Cut", 
            variable=self.lowcut_var, 
            command=self.update_equalizer,
            bootstyle="info"
        )
        self.lowcut_checkbox.grid(row=1, column=0, sticky="w", pady=2)

        # Enable High Cut
        self.highcut_var = ttk.IntVar(value=self.view_model.highcut_apply)
        self.highcut_checkbox = ttk.Checkbutton(
            self.turnon_frame, 
            text="Enable High Cut", 
            variable=self.highcut_var, 
            command=self.update_equalizer,
            bootstyle="warning"
        )
        self.highcut_checkbox.grid(row=2, column=0, sticky="w", pady=2)

        # Các slider band
        self.create_sliders()

        # Low cut và High cut slider
        self.freqcut_frame = ttk.Frame(self.first_row_frame)
        self.freqcut_frame.grid(row=0, column=len(self.view_model.band_gains) + 1, padx=5, sticky="n")

        # ttk.Label(self.vol_frame, text="Low Cut (kHz)").pack(side=LEFT, padx=10)
        self.lowcut_slider = ttk.Scale(
            self.freqcut_frame, 
            from_=1, 
            to=100, 
            orient=HORIZONTAL, 
            # label="Low Cut (Hz)",
            length=150,
            bootstyle="primary"
        )
        self.lowcut_slider.bind("<ButtonRelease-1>", lambda e: self.update_equalizer())
        self.lowcut_slider.grid(row=0, column=0, pady=5)
        self.lowcut_slider.set(self.view_model.lowcut_freq) 

        # ttk.Label(self.vol_frame, text="High Cut (kHz)").pack(side=LEFT, padx=10)
        self.highcut_slider = ttk.Scale(
            self.freqcut_frame, 
            from_=5, 
            to=20, 
            # resolution=1, 
            orient=HORIZONTAL, 
            # label="High Cut (kHz)",
            length=150,
            bootstyle="danger"
        )
        self.highcut_slider.bind("<ButtonRelease-1>", lambda e: self.update_equalizer())
        self.highcut_slider.grid(row=1, column=0, pady=5)
        self.highcut_slider.set(self.view_model.highcut_freq) 

        self.view_model.add_view_listener(self)

    def on_close(self):
        print("Closing basic equalizer...")
        self.view_model.on_close()
        
    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

    def create_sliders(self):
        """Tạo các slider cho mỗi band từ band_gains"""
        for idx, (band_name, gain) in enumerate(self.view_model.band_gains.items(), start=1):
            frame = ttk.Frame(self.first_row_frame)
            frame.grid(row=0, column=idx, padx=5, sticky="n")

            slider = ttk.Scale(
                frame, 
                from_=-24, 
                to=24, 
                orient=VERTICAL, 
                bootstyle="info"
            )
            slider.bind("<ButtonRelease-1>", lambda e, band=band_name: self.update_equalizer(band))
            slider.set(gain)
            slider.grid(row=0, column=0, pady=5)

            label = ttk.Label(frame, text=band_name)
            label.grid(row=1, column=0, pady=2)
            
            self.sliders[band_name] = slider
            self.band_labels[band_name] = label

    def update_equalizer(self, band=None):
        gains = {band: slider.get() for band, slider in self.sliders.items()}
        self.view_model.update_equalizer_info(
            self.eqapply_var.get(),
            gains,
            self.lowcut_var.get(),
            self.lowcut_slider.get(),
            self.highcut_var.get(),
            self.highcut_slider.get(),
        )

    def update_view(self, event_name, data):
        if event_name == "eq_info_changed":
            print("eq_info_changed in equalizer_basic_view")
            self.eqapply_var.set(self.view_model.eq_apply)
            self.lowcut_var.set(self.view_model.lowcut_apply)
            self.lowcut_slider.set(self.view_model.lowcut_freq)
            self.highcut_var.set(self.view_model.highcut_apply)
            self.highcut_slider.set(self.view_model.highcut_freq)
            [slider.set(self.view_model.band_gains[band]) for band, slider in self.sliders.items()]
