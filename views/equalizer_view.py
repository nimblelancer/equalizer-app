import tkinter as tk
from viewmodels.equalizer_advanced_viewmodel import EqualizerViewModel2
from tkinter import Toplevel
from views.equalizer_view2 import EqualizerView2

class EqualizerView:
    def __init__(self, root, view_model: EqualizerViewModel2):
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Dòng đầu tiên
        self.first_row_frame = tk.Frame(self.frame)
        self.first_row_frame.pack()

        self.turnon_frame = tk.Frame(self.first_row_frame, width=200)
        self.turnon_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        self.turnon_frame.pack_propagate(0)

        # Checkbutton để bật/tắt High Cut
        self.eqapply_var = tk.IntVar()
        self.eq_checkbox = tk.Checkbutton(self.turnon_frame, text="Enable Equalizer", variable=self.eqapply_var, command=self.update_equalizer)
        self.eq_checkbox.pack()
        
        # Checkbutton để bật/tắt Low Cut
        self.lowcut_var = tk.IntVar()
        self.lowcut_checkbox = tk.Checkbutton(self.turnon_frame, text="Enable Low Cut", variable=self.lowcut_var, command=self.update_equalizer)
        self.lowcut_checkbox.pack()
        
        # Checkbutton để bật/tắt High Cut
        self.highcut_var = tk.IntVar()
        self.highcut_checkbox = tk.Checkbutton(self.turnon_frame, text="Enable High Cut", variable=self.highcut_var, command=self.update_equalizer)
        self.highcut_checkbox.pack()

        self.more_button = tk.Button(self.turnon_frame, text="Advance Settings", width=13, command=self.open_more)
        self.more_button.pack()
        


        # Thanh trượt equalizer bass
        self.bass_frame = tk.Frame(self.first_row_frame, width=100)
        self.bass_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        self.bass_frame.pack_propagate(0)
        self.bass_slider = tk.Scale(self.bass_frame, from_=-24, to=24, resolution=1, orient="vertical", command=self.update_equalizer)
        self.bass_slider.pack()
        self.bass_slider.set(1)
        self.bass_label = tk.Label(self.bass_frame, text="Bass")
        self.bass_label.pack()

        # Thanh trượt equalizer mid-bass
        self.midbass_frame = tk.Frame(self.first_row_frame, width=100)
        self.midbass_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        self.midbass_slider = tk.Scale(self.midbass_frame, from_=-24, to=24, resolution=0.1, orient="vertical", command=self.update_equalizer)
        self.midbass_slider.pack()
        self.midbass_slider.set(1)
        self.midbass_label = tk.Label(self.midbass_frame, text="Mid-bass")
        self.midbass_label.pack()
        
        # Thanh trượt equalizer mid
        self.mid_frame = tk.Frame(self.first_row_frame, width=100)
        self.mid_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        self.mid_slider = tk.Scale(self.mid_frame, from_=-24, to=24, resolution=0.1, orient="vertical", command=self.update_equalizer)
        self.mid_slider.pack()
        self.mid_slider.set(1)
        self.mid_label = tk.Label(self.mid_frame, text="Midrange")
        self.mid_label.pack()

        # Thanh trượt equalizer upper mid
        self.uppermid_frame = tk.Frame(self.first_row_frame, width=100)
        self.uppermid_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        self.uppermid_slider = tk.Scale(self.uppermid_frame, from_=0, to=2, resolution=0.1, orient="vertical", command=self.update_equalizer)
        self.uppermid_slider.pack()
        self.uppermid_slider.set(1)
        self.uppermid_label = tk.Label(self.uppermid_frame, text="Upper Mid")
        self.uppermid_label.pack()
        
        # Thanh trượt equalizer treble
        self.treble_frame = tk.Frame(self.first_row_frame, width=100)
        self.treble_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        self.treble_slider = tk.Scale(self.treble_frame, from_=-24, to=24, resolution=0.1, orient="vertical", command=self.update_equalizer)
        self.treble_slider.pack()
        self.treble_slider.set(1)
        self.treble_label = tk.Label(self.treble_frame, text="Treble")
        self.treble_label.pack()

        self.freqcut_frame = tk.Frame(self.first_row_frame, width=200)
        self.freqcut_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y, expand=False)
        self.freqcut_frame.pack_propagate(0)

        # Thanh trượt Low Cut
        self.lowcut_slider = tk.Scale(self.freqcut_frame, from_=1, to=100, orient="horizontal", label="Low Cut (Hz)", command=self.update_equalizer)
        self.lowcut_slider.pack()
        self.lowcut_slider.set(20) 

        # Thanh trượt High Cut
        self.highcut_slider = tk.Scale(self.freqcut_frame, from_=5, to=20, resolution=1, orient="horizontal", label="High Cut (kHz)", command=self.update_equalizer)
        self.highcut_slider.pack()
        self.highcut_slider.set(15) 

        self.view_model = view_model
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    # self, eq_apply, bass_gain, midbass_gain, midrange_gain, uppermid_gain, treeble_gain, lowcut_applied, lowcut_freq, highcut_applied, highcut_freq
    def update_equalizer(self, event=None):
        self.view_model.update_equalizer_info (
            self.eqapply_var.get(),
            self.bass_slider.get(),
            self.midbass_slider.get(),
            self.mid_slider.get(),
            self.uppermid_slider.get(),
            self.treble_slider.get(),
            self.lowcut_var.get(),
            self.lowcut_slider.get(),
            self.highcut_var.get(),
            self.highcut_slider.get(),
            
        )


    def open_more(self):
        # Tạo cửa sổ con mới
        new_window = Toplevel(self.frame)  # 'root' là cửa sổ chính
        new_window.title("EQ Setting")
        
        equalizer_view2 = EqualizerView2(new_window, self.view_model)