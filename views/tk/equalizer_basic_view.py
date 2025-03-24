import tkinter as tk
from viewmodels.equalizer_basic_viewmodel import EqualizerBasicViewModel

class EqualizerBasicView:
    def __init__(self, root, view_model: EqualizerBasicViewModel):
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.view_model = view_model
        
        # Khởi tạo các slider và label cho các band từ band_gains
        self.sliders = {}
        self.band_labels = {}
        
        self.first_row_frame = tk.Frame(self.frame)
        self.first_row_frame.pack()

        self.turnon_frame = tk.Frame(self.first_row_frame, width=200)
        self.turnon_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        # self.turnon_frame.pack_propagate(0)

        # Checkbutton để bật/tắt Equalizer
        self.eqapply_var = tk.IntVar()
        self.eqapply_var.set(self.view_model.eq_apply)
        self.eq_checkbox = tk.Checkbutton(self.turnon_frame, text="Enable Equalizer", variable=self.eqapply_var, command=self.update_equalizer)
        self.eq_checkbox.pack()

        # Checkbutton để bật/tắt Low Cut
        self.lowcut_var = tk.IntVar()
        self.lowcut_var.set(self.view_model.lowcut_apply)
        self.lowcut_checkbox = tk.Checkbutton(self.turnon_frame, text="Enable Low Cut", variable=self.lowcut_var, command=self.update_equalizer)
        self.lowcut_checkbox.pack()
        
        # Checkbutton để bật/tắt High Cut
        self.highcut_var = tk.IntVar()
        self.highcut_var.set(self.view_model.highcut_apply)
        self.highcut_checkbox = tk.Checkbutton(self.turnon_frame, text="Enable High Cut", variable=self.highcut_var, command=self.update_equalizer)
        self.highcut_checkbox.pack()

        # Khởi tạo các slider và label cho các band (bass, mid-bass, midrange, uppermid, treble)
        self.create_sliders()

        # Thanh trượt Low Cut và High Cut
        self.freqcut_frame = tk.Frame(self.first_row_frame)
        self.freqcut_frame.pack(side=tk.LEFT, padx=5)

        self.lowcut_slider = tk.Scale(self.freqcut_frame, from_=1, to=100, orient="horizontal", label="Low Cut (Hz)")
        self.lowcut_slider.bind("<ButtonRelease-1>", lambda event: self.update_equalizer())
        self.lowcut_slider.pack()
        self.lowcut_slider.set(self.view_model.lowcut_freq) 

        self.highcut_slider = tk.Scale(self.freqcut_frame, from_=5, to=20, resolution=1, orient="horizontal", label="High Cut (kHz)")
        self.highcut_slider.bind("<ButtonRelease-1>", lambda event: self.update_equalizer())
        self.highcut_slider.pack()
        self.highcut_slider.set(self.view_model.highcut_freq) 

        self.view_model.add_view_listener(self)

    def create_sliders(self):
        """Tạo các slider cho mỗi band từ band_gains"""
        for band_name, gain in self.view_model.band_gains.items():
            frame = tk.Frame(self.first_row_frame)
            frame.pack(side=tk.LEFT, padx=5)
            
            # Tạo slider cho band
            slider = tk.Scale(frame, from_=-24, to=24, resolution=1, orient="vertical")
            slider.bind("<ButtonRelease-1>", lambda event, band=band_name: self.update_equalizer(band))
            slider.set(gain)  # Thiết lập giá trị khởi tạo từ band_gains
            slider.pack()
            
            # Thêm label cho band
            label = tk.Label(frame, text=band_name)
            label.pack()
            
            # Lưu trữ slider và label
            self.sliders[band_name] = slider
            self.band_labels[band_name] = label

    def update_equalizer(self, event=None):
        """Cập nhật bộ equalizer khi người dùng thay đổi các tham số"""
        # Thu thập giá trị từ các slider và checkbutton
        gains = {band: slider.get() for band, slider in self.sliders.items()}
        self.view_model.update_equalizer_info(
            self.eqapply_var.get(),
            gains,
            self.lowcut_var.get(),
            self.lowcut_slider.get(),
            self.highcut_var.get(),
            self.highcut_slider.get(),
        )

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def update_view(self, event_name, data):
        if event_name == "eq_info_changed":
            print("eq_info_changed in equalizer_basic_view")
            self.eqapply_var.set(self.view_model.eq_apply)
            self.lowcut_var.set(self.view_model.lowcut_apply)
            self.lowcut_slider.set(self.view_model.lowcut_freq)
            self.highcut_var.set(self.view_model.highcut_apply)
            self.highcut_slider.set(self.view_model.highcut_freq)
            [slider.set(self.view_model.band_gains[band]) for band, slider in self.sliders.items()]
