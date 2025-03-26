import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from viewmodels.equalizer_basic_viewmodel import EqualizerBasicViewModel

class EqualizerBasicView(ttk.LabelFrame):
    def __init__(self, root, view_model):
        
        super().__init__(root, text="Equalizer")
        self.root = root
        self.view_model = view_model

        # Cấu hình frame chính để nằm giữa
        self.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
       
        self.columnconfigure(0, weight=1)

         # ✅ Preset Selection (Hàng 0)
        self.preset_frame = ttk.Frame(self)
        self.preset_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(self.preset_frame, text="Presets:", foreground="white").grid(row=0, column=0, padx=10)
        self.selected_preset = ttk.StringVar(value="Pop")

        presets = ["Rock", "Ballad", "EDM", "Pop"]
        preset_buttons = ttk.Frame(self.preset_frame)
        preset_buttons.grid(row=0, column=1, padx=2, sticky="ew")

        for i, preset in enumerate(presets):
            ttk.Radiobutton(
                preset_buttons, text=preset, value=preset, variable=self.selected_preset,
                bootstyle="primary", padding=(10, 3)
            ).grid(row=0, column=i, padx=5)

        # ✅ Khung chứa sliders & controls
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=1, column=0, sticky="ew")
        self.main_frame.columnconfigure(0, weight=1)


        # Các slider cơ bản
        self.sliders = {}
        # Các slider band
        self.slider_frame = ttk.Frame(self)
        self.slider_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
        self.create_sliders()



        self.first_row_frame = ttk.Frame(self)
        self.first_row_frame.grid(row=2, column=0)

        self.turnon_frame = ttk.Frame(self.first_row_frame)
        self.turnon_frame.grid(row=2, column=0, padx=5)

        # Enable Equalizer
        self.eqapply_var = ttk.IntVar(value=self.view_model.eq_apply)
        self.eq_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Enable Equalizer",
            variable=self.eqapply_var,
            command=self.update_equalizer,
            bootstyle="success"
        )
        self.eq_checkbox.grid(row=4, column=0, pady=2)       

        

         # Enable Low Cut
        self.lowcut_var = ttk.IntVar(value=self.view_model.lowcut_apply)
        self.lowcut_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Enable Low Cut",
            variable=self.lowcut_var,
            command=self.update_equalizer,
        )
        self.lowcut_checkbox.grid(row=5, column=0, pady=2)

        # Enable High Cut
        self.highcut_var = ttk.IntVar(value=self.view_model.highcut_apply)
        self.highcut_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Enable High Cut",
            variable=self.highcut_var,
            command=self.update_equalizer,
            bootstyle="primary"
        )
        self.highcut_checkbox.grid(row=6, column=0, pady=2)

        # Low cut và High cut slider
        self.freqcut_frame = ttk.Frame(self.first_row_frame)
        self.freqcut_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        self.lowcut_slider = ttk.Scale(
            self.freqcut_frame,
            from_=1,
            to=100,
            orient=HORIZONTAL,
            length=150,
            bootstyle="primary"
        )
        self.lowcut_slider.bind("<ButtonRelease-1>", lambda e: self.update_equalizer())
        self.lowcut_slider.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.lowcut_slider.set(self.view_model.lowcut_freq)

        self.highcut_slider = ttk.Scale(
            self.freqcut_frame,
            from_=5,
            to=20,
            orient=HORIZONTAL,
            length=150,
            bootstyle="primary"
        )
        self.highcut_slider.bind("<ButtonRelease-1>", lambda e: self.update_equalizer())
        self.highcut_slider.grid(row=0, column=1, pady=10, padx=10, sticky="e")
        self.highcut_slider.set(self.view_model.highcut_freq)

        self.view_model.add_view_listener(self)

    def on_close(self):
        print("Closing basic equalizer...")
        self.view_model.on_close()

    def create_sliders(self):
        """Tạo các slider cho mỗi band từ band_gains và căn giữa chúng"""

        num_bands = len(self.view_model.band_gains)
        self.slider_frame.columnconfigure(tuple(range(num_bands)), weight=1)

        for idx, (band_name, gain) in enumerate(self.view_model.band_gains.items()):
            frame = ttk.Frame(self.slider_frame)
            frame.grid(row=0, column=idx, padx=10, sticky="nsew")
            frame.columnconfigure(0, weight=1)

            slider = ttk.Scale(
                frame,
                from_=-12,
                to=12,
                orient=VERTICAL,
                bootstyle="primary",
            )
            slider.bind("<ButtonRelease-1>", lambda e, band=band_name: self.update_equalizer(band))
            slider.set(gain)
            slider.grid(row=0, column=0, pady=5, sticky="ns")

            label = ttk.Label(frame, text=band_name, anchor="center")
            label.grid(row=1, column=0, pady=2, sticky="n")

            self.sliders[band_name] = slider

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

            for band, slider in self.sliders.items():
                slider.set(self.view_model.band_gains[band])