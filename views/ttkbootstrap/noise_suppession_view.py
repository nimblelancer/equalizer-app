import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import simpledialog, messagebox


class NoiseSuppressionView(ttk.Frame):
    def __init__(self, root, view_model):
        super().__init__(root)
        self.root = root
        self.view_model = view_model
        self.init_ui()

    def update_label(self, slider, label):
        label.config(text=f"{round(slider.get(), 1)}")

    def init_ui(self):
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure(tuple(range(20)), weight=1)
        self.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # Highcut Filter
        self.highcut_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable Highcut Filter", variable=self.highcut_var, command=self.update_noise_setting).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.highcut_slider = ttk.Scale(self, from_=10, to_=200, orient="horizontal", command=lambda v: self.update_label(self.highcut_slider, self.highcut_label))
        self.highcut_slider.grid(row=1, column=0,  sticky="we", padx=10, pady=5)
        self.highcut_label = ttk.Label(self, text="20")
        self.highcut_label.grid(row=1, column=1, padx=5)
        self.highcut_var.set(self.view_model.highcut_enabled)
        self.highcut_slider.set(self.view_model.highcut_freq)

        # Lowcut Filter
        self.lowcut_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable Lowcut Filter", variable=self.lowcut_var,  command=self.update_noise_setting).grid(row=2, column=0, sticky="w" , padx=10, pady=5,)
        self.lowcut_slider = ttk.Scale(self, from_=20, to_=2000, orient="horizontal", command=lambda v: self.update_label(self.lowcut_slider, self.lowcut_label))
        self.lowcut_slider.grid(row=3, column=0, sticky="we", padx=10, pady=5)
        self.lowcut_label = ttk.Label(self, text="20")
        self.lowcut_label.grid(row=3, column=1, padx=5)
        self.lowcut_var.set(self.view_model.lowcut_enabled)
        self.lowcut_slider.set(self.view_model.lowcut_freq)

        # Amplitude Cut
        self.amplitude_cut_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable Amplitude Cut", variable=self.amplitude_cut_var,  command=self.update_noise_setting).grid(row=4, column=0, sticky="w", padx=10, pady=5,)
        self.amplitude_cut_slider = ttk.Scale(self, from_=0, to_=2000, orient="horizontal", command=lambda v: self.update_label(self.amplitude_cut_slider, self.amplitude_cut_label))
        self.amplitude_cut_slider.grid(row=5, column=0, sticky="we", padx=10, pady=5)
        self.amplitude_cut_label = ttk.Label(self, text="0.0")
        self.amplitude_cut_label.grid(row=5, column=1, padx=5)
        self.amplitude_cut_var.set(self.view_model.amplitude_cut_enabled)
        self.amplitude_cut_slider.set(self.view_model.amplitude_cut)

        # Hum Frequency Cut
        self.hum_cut_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable Hum Frequency Cut", variable=self.hum_cut_var, command=self.update_noise_setting).grid(row=6, column=0, sticky="w", padx=10, pady=5, )
        self.hum_freq_slider = ttk.Scale(self, from_=20, to_=2000, orient="horizontal", command=lambda v: self.update_label(self.hum_freq_slider, self.hum_freq_label))
        self.hum_freq_slider.grid(row=7, column=0, sticky="we", padx=10, pady=5)
        self.hum_freq_label = ttk.Label(self, text="20")
        self.hum_freq_label.grid(row=7, column=1, padx=5)
        self.hum_cut_var.set(self.view_model.hum_cut_enabled)
        self.hum_freq_slider.set(self.view_model.hum_freq)

        # Band Stop Filter
        self.bandstop_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable Band Stop Filter", variable=self.bandstop_var,  command=self.update_noise_setting).grid(row=8, column=0, sticky="w", padx=10, pady=5,)
        ttk.Button(self, text="Add Band Stop Frequency", bootstyle="outline-primary", command=self.add_bandstop).grid(row=9, column=0, sticky="we", padx=10, pady=5,  )
        ttk.Label(self, text="Bandstop Frequencies:").grid(row=10, column=0, sticky="w", padx=10, pady=5)
        ttk.Button(self, text="Remove Selected Bandstop Frequency", bootstyle="outline-warning", command=self.remove_bandstop).grid(row=11, column=0, sticky="we", padx=10, pady=5, )
        self.bandstop_var.set(self.view_model.bandstop_enabled)
        # Band Notch Filter
        self.bandnotch_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable Band Notch Filter", variable=self.bandnotch_var).grid(row=12, column=0, sticky="w", padx=10, pady=5)
        ttk.Button(self, text="Add Notch Frequency", bootstyle="outline-primary", command=self.add_bandnotch).grid(row=13, column=0, sticky="we", padx=10, pady=5, )
        ttk.Label(self, text="Bandnotch Frequencies:").grid(row=14, column=0, sticky="w", padx=10, pady=5)
        ttk.Button(self, text="Remove Selected Notch Frequency", bootstyle="outline-warning", command=self.remove_bandnotch).grid(row=15, column=0, sticky="we", padx=10, pady=5, )
        self.bandnotch_var.set(self.view_model.bandnotch_enabled)
        # Q Factor Slider
        ttk.Label(self, text="Q Factor").grid(row=16, column=0, sticky="w", padx=10, pady=5)
        self.q_factor_slider = ttk.Scale(self, from_=0.1, to_=30, orient="horizontal", command=lambda v: self.update_label(self.q_factor_slider, self.q_factor_label))
        self.q_factor_slider.grid(row=17, column=0, sticky="we", padx=10, pady=5)
        self.q_factor_label = ttk.Label(self, text="0.1")
        self.q_factor_label.grid(row=17, column=1, padx=5)
        self.q_factor_slider.set(self.view_model.q_factor)

        # LMS Filter
        self.lms_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable LMS Filter", variable=self.lms_var, command=self.update_noise_setting,).grid(row=18, column=0, sticky="w",  padx=10, pady=5)
        self.lms_var.set(self.view_model.lms_enabled)
        # Apply Button
        # ttk.Button(self, text="Apply Filters", bootstyle="outline-success").grid(row=19, column=0, sticky="we", pady=10, padx=10)
        self.highcut_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.lowcut_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.amplitude_cut_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.hum_freq_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.q_factor_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())

    def on_filter_change(self):
        self.view_model.update_model_from_view(
            self.highcut_var.get(),
            self.lowcut_var.get(),
            self.amplitude_cut_var.get(),
            self.hum_cut_var.get(),
            self.bandstop_var.get(),
            self.bandnotch_var.get(),
            self.lms_var.get(),
            self.highcut_slider.get(),
            self.lowcut_slider.get(),
            self.hum_freq_slider.get(),
            self.q_factor_slider.get(),
            self.amplitude_cut_slider.get()
        )

    def add_bandstop(self):
        freq = simpledialog.askinteger("Input", "Enter Band Stop Frequency (Hz):")
        if freq is not None:
            self.view_model.add_bandstop(freq)
        self.update_bandstop_display()

    def remove_bandstop(self):
        # Tạo giao diện chọn tần số cần xóa
        freq = simpledialog.askinteger("Input", "Enter Band Stop Frequency to Remove (Hz):")
        if freq is not None:
            self.view_model.remove_bandstop(freq)
        self.update_bandstop_display()

    def add_bandnotch(self):
        freq = simpledialog.askinteger("Input", "Enter Notch Frequency (Hz):")
        if freq is not None:
            self.view_model.add_bandnotch(freq)
        self.update_bandnotch_display()

    def remove_bandnotch(self):
        # Tạo giao diện chọn tần số cần xóa
        freq = simpledialog.askinteger("Input", "Enter Notch Frequency to Remove (Hz):")
        if freq is not None:
            self.view_model.remove_bandnotch(freq)
        self.update_bandnotch_display()

    def apply_filters(self):
        filters_applied = self.view_model.get_filter_settings()
        settings_summary = "\n".join([f"{key}: {value}" for key, value in filters_applied.items()])
        messagebox.showinfo("Filter Settings", settings_summary)

    def update_bandstop_display(self):
        freqs = ", ".join(map(str, self.view_model.model.bandstop_list))
        self.bandstop_label.config(text=f"Bandstop Frequencies: {freqs}")

    def update_bandnotch_display(self):
        freqs = ", ".join(map(str, self.view_model.model.bandnotch_list))
        self.bandnotch_label.config(text=f"Bandnotch Frequencies: {freqs}")

    def update_noise_setting(self):
        self.view_model.update_model_from_view(
            self.highcut_var.get(),
            self.highcut_slider.get(),
            self.lowcut_var.get(),
            self.lowcut_slider.get(),
            self.amplitude_cut_var.get(),
            self.amplitude_cut_slider.get(),
            self.hum_cut_var.get(),
            self.hum_freq_slider.get(),
            self.bandstop_var.get(),
            None,
            self.bandnotch_var.get(),
            None,
            self.q_factor_slider.get(),
            self.lms_var.get()
        )