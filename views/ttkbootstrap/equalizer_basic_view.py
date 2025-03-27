from tkinter import IntVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from viewmodels.equalizer_basic_viewmodel import EqualizerBasicViewModel
from ttkbootstrap.icons import Emoji
class EqualizerBasicView(ttk.LabelFrame):
    def __init__(self, root, view_model: EqualizerBasicViewModel):
        
        super().__init__(root, text="Equalizer")
        self.root = root
        self.view_model = view_model

        self.columnconfigure((0,1,2), weight=1)  # Giúp LabelFrame mở rộng theo chiều ngang
        self.rowconfigure((0,1,2,3,4), weight=1)

        # Cấu hình frame chính để nằm giữa
        self.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
       
        self.columnconfigure(0, weight=1)

         # ✅ Preset Selection (Hàng 0)
        self.preset_frame = ttk.Frame(self)
        self.preset_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")
        
        ttk.Label(self.preset_frame, text="Presets:", foreground="white").grid(row=0, column=0, padx=10)
        self.selected_preset = ttk.StringVar(value="EDM")

        presets = ["Rock", "Ballad", "EDM", "Pop"]
        preset_buttons = ttk.Frame(self.preset_frame)
        preset_buttons.grid(row=0, column=1, padx=2, sticky="ew")

        for i, preset in enumerate(presets):
            ttk.Radiobutton(
                preset_buttons, text=preset, value=preset, variable=self.selected_preset,
                bootstyle="primary", padding=(10, 3),
                command=self.apply_preset
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


        # Checkbox
        self.first_row_frame = ttk.Frame(self)
        self.first_row_frame.grid(row=2, column=0, padx=5, pady=5)

        self.turnon_frame = ttk.Frame(self.first_row_frame)
        self.turnon_frame.grid(row=2, column=0)

        # Enable Equalizer
        self.eqapply_var = ttk.IntVar(value=self.view_model.eq_apply)
        self.eq_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Enable Equalizer",
            variable=self.eqapply_var,
            command=self.update_equalizer,
            bootstyle="success"
        )
        self.eq_checkbox.grid(row=0, column=0, padx=5, pady=2, sticky="w")

        # Enable Low Cut
        self.lowcut_var = ttk.IntVar(value=self.view_model.lowcut_apply)
        
        self.lowcut_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Enable Low Cut",
            variable=self.lowcut_var,
            command=self.update_equalizer,
        )
        self.lowcut_checkbox.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        # Enable High Cut
        self.highcut_var = ttk.IntVar(value=self.view_model.highcut_apply)
        self.highcut_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Enable High Cut",
            variable=self.highcut_var,
            command=self.update_equalizer,
            bootstyle="primary"
        )
        self.highcut_checkbox.grid(row=0, column=2, padx=5, pady=2, sticky="w")

        # Small Clip
        self.smallclip_var = ttk.IntVar(value=0)
        self.smallclip_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Small Clip",
            variable=self.smallclip_var,
            command=self.update_adaptive_settings
        )
        self.smallclip_checkbox.grid(row=1, column=0, padx=5, pady=2, sticky="w")

        # Adaptive LMS
        self.adaptive_lms_var = ttk.IntVar(value=0)
        self.adaptive_lms_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Adaptive LMS",
            variable=self.adaptive_lms_var,
            command=self.update_adaptive_settings
        )
        self.adaptive_lms_checkbox.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Adaptive Notch
        self.adaptive_notch_var = ttk.IntVar(value=0)
        self.adaptive_notch_checkbox = ttk.Checkbutton(
            self.turnon_frame,
            text="Adaptive Notch",
            variable=self.adaptive_notch_var,
            command=self.update_adaptive_settings
        )
        self.adaptive_notch_checkbox.grid(row=1, column=2, padx=5, pady=2, sticky="w")

        # Low cut và High cut slider
        self.freqcut_frame = ttk.Frame(self.first_row_frame)
        self.freqcut_frame.grid(row=3, column=0, columnspan=2, pady=5)

        # Label hiển thị Low Cut
        self.lowcut_label = ttk.Label(self.freqcut_frame, text="Low Cut:")
        self.lowcut_label.grid(row=0, column=0, padx=(10, 5), sticky="e")

        # Giá trị hiển thị của Low Cut
        self.lowcut_value = IntVar(value=self.view_model.lowcut_freq)
        self.lowcut_value_label = ttk.Label(self.freqcut_frame, textvariable=self.lowcut_value)
        self.lowcut_value_label.grid(row=0, column=2, padx=(5, 10), sticky="w")

        # Low Cut Slider
        self.lowcut_slider = ttk.Scale(
            self.freqcut_frame,
            from_=1,
            to=100,
            orient=HORIZONTAL,
            length=150,
            bootstyle="primary",
            command=lambda v: self.lowcut_value.set(int(float(v)))  # Cập nhật giá trị
        )
        self.lowcut_slider.bind("<ButtonRelease-1>", lambda e: self.update_equalizer())
        self.lowcut_slider.grid(row=0, column=1, pady=10, padx=5, sticky="w")
        self.lowcut_slider.set(self.view_model.lowcut_freq)

        # Label hiển thị High Cut
        self.highcut_label = ttk.Label(self.freqcut_frame, text="High Cut:")
        self.highcut_label.grid(row=1, column=0, padx=(10, 5), sticky="e")

        # Giá trị hiển thị của High Cut
        self.highcut_value = IntVar(value=self.view_model.highcut_freq)
        self.highcut_value_label = ttk.Label(self.freqcut_frame, textvariable=self.highcut_value)
        self.highcut_value_label.grid(row=1, column=2, padx=(5, 10), sticky="w")

        # High Cut Slider
        self.highcut_slider = ttk.Scale(
            self.freqcut_frame,
            from_=5,
            to=20,
            orient=HORIZONTAL,
            length=150,
            bootstyle="primary",
            command=lambda v: self.highcut_value.set(int(float(v)))  # Cập nhật giá trị
        )
        self.highcut_slider.bind("<ButtonRelease-1>", lambda e: self.update_equalizer())
        self.highcut_slider.grid(row=1, column=1, pady=10, padx=5, sticky="e")
        self.highcut_slider.set(self.view_model.highcut_freq)

        self.view_model.add_view_listener(self)

    def on_close(self):
        print("Closing basic equalizer...")
        self.view_model.on_close()

    def create_sliders(self):
        """Tạo sliders với nhãn dB bên trái và nhãn band_name đúng vị trí"""

        num_bands = len(self.view_model.band_gains)
        self.slider_frame.columnconfigure(tuple(range(num_bands + 1)), weight=1)

        # Nhãn dB bên trái
        db_labels = ["+12 dB", "+6 dB", "0 dB", "-6 dB", "-12 dB"]
        label_frame = ttk.Frame(self.slider_frame)
        label_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ns")

        for db_text in db_labels:
            ttk.Label(label_frame, text=db_text, anchor="e").pack(fill="y", expand=True )

        # Tạo sliders với band_name đúng cột
        for idx, (band_name, gain) in enumerate(self.view_model.band_gains.items()):
            self.slider_frame.columnconfigure(idx + 1, weight=1)  # Đảm bảo phân bổ đều cột

            frame = ttk.Frame(self.slider_frame)
            frame.grid(row=0, column=idx + 1, padx=10, sticky="n", pady=10)

            # Giá trị hiển thị của slider (làm tròn)
            # value_var = ttk.DoubleVar(value=round(gain, 2))
            # value_label = ttk.Label(frame, textvariable=value_var, anchor="center")
            # value_label.pack()

            # Slider
            slider = ttk.Scale(
                frame, 
                from_=12, 
                to=-12, 
                orient=VERTICAL, 
                bootstyle="primary", 
                length=200,
                # command=lambda v, var=value_var: var.set(int(round(float(v), 1)))  # Cập nhật giá trị hiển thị (làm tròn)
            )
            slider.bind("<ButtonRelease-1>", lambda e, band=band_name: self.update_equalizer(band))
            slider.set(gain)
            slider.pack()

            # Nhãn band_name đặt đúng dưới slider
            ttk.Label(self.slider_frame, text=band_name, anchor="center").grid(row=1, column=idx + 1, sticky="n")

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

    def update_adaptive_settings(self):
        pass

    def apply_preset(self):
        """Update all band parameters based on the selected preset"""
        self.view_model.apply_equalizer_preset(
            self.eqapply_var.get(),
            self.selected_preset.get().lower(),
            self.lowcut_var.get(),
            self.lowcut_slider.get(),
            self.highcut_var.get(),
            self.highcut_slider.get(),
        )