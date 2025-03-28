import tkinter as tk
from tkinter import simpledialog, messagebox

# 3. View: Quản lý giao diện người dùng.
class NoiseSuppressionView(tk.Frame):
    def __init__(self, master, view_model):
        super().__init__(master)
        self.master = master
        self.view_model = view_model
        self.init_ui()

    def init_ui(self):
        self.master.title("Audio Filter Settings")
        self.master.geometry("500x600")

        # Highcut Filter
        self.highcut_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Enable Highcut Filter", variable=self.highcut_var, command=self.update_noise_setting).pack(anchor="w")
        self.highcut_slider = tk.Scale(self.master, from_=10, to_=200, orient="horizontal", label="Highcut Frequency (Hz)")
        self.highcut_slider.pack()
        self.highcut_var.set(self.view_model.highcut_enabled)
        self.highcut_slider.set(self.view_model.highcut_freq)
        
        # Lowcut Filter
        self.lowcut_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Enable Lowcut Filter", variable=self.lowcut_var, command=self.update_noise_setting).pack(anchor="w")
        self.lowcut_slider = tk.Scale(self.master, from_=20, to_=2000, orient="horizontal", label="Lowcut Frequency (Hz)")
        self.lowcut_slider.pack()
        self.lowcut_var.set(self.view_model.lowcut_enabled)
        self.lowcut_slider.set(self.view_model.lowcut_freq)

        # Amplitude Cut
        self.amplitude_cut_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Enable Amplitude Cut", variable=self.amplitude_cut_var, command=self.update_noise_setting).pack(anchor="w")
        self.amplitude_cut_slider = tk.Scale(self.master, from_=0, to_=2000, orient="horizontal", label="Amplitude Cut Level")
        self.amplitude_cut_slider.pack()
        self.amplitude_cut_var.set(self.view_model.amplitude_cut_enabled)
        self.amplitude_cut_slider.set(self.view_model.amplitude_cut)

        # Hum Frequency Cut
        self.hum_cut_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Enable Hum Frequency Cut", variable=self.hum_cut_var, command=self.update_noise_setting).pack(anchor="w")
        self.hum_freq_slider = tk.Scale(self.master, from_=20, to_=2000, orient="horizontal", label="Hum Frequency (Hz)")
        self.hum_freq_slider.pack()
        self.hum_cut_var.set(self.view_model.hum_cut_enabled)
        self.hum_freq_slider.set(self.view_model.hum_freq)

        # Band Stop Filter
        self.bandstop_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Enable Band Stop Filter", variable=self.bandstop_var, command=self.update_noise_setting).pack(anchor="w")
        self.bandstop_button = tk.Button(self.master, text="Add Band Stop Frequency", command=self.add_bandstop)
        self.bandstop_button.pack()
        self.bandstop_label = tk.Label(self.master, text="Bandstop Frequencies: ")
        self.bandstop_label.pack(anchor="w")
        self.remove_bandstop_button = tk.Button(self.master, text="Remove Selected Bandstop Frequency", command=self.remove_bandstop)
        self.remove_bandstop_button.pack()
        self.bandstop_var.set(self.view_model.bandstop_enabled)

        # Band Notch Filter
        self.bandnotch_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Enable Band Notch Filter", variable=self.bandnotch_var, command=self.update_noise_setting).pack(anchor="w")
        self.bandnotch_button = tk.Button(self.master, text="Add Notch Frequency", command=self.add_bandnotch)
        self.bandnotch_button.pack()
        self.bandnotch_label = tk.Label(self.master, text="Bandnotch Frequencies: ")
        self.bandnotch_label.pack(anchor="w")
        self.remove_bandnotch_button = tk.Button(self.master, text="Remove Selected Notch Frequency", command=self.remove_bandnotch)
        self.remove_bandnotch_button.pack()
        self.bandnotch_var.set(self.view_model.bandnotch_enabled)

        # Q Factor Slider
        self.q_factor_slider = tk.Scale(self.master, from_=0.1, to_=30, orient="horizontal", resolution=0.1, label="Q Factor")
        self.q_factor_slider.pack()
        self.q_factor_slider.set(self.view_model.q_factor)
        

        # LMS Filter
        self.lms_var = tk.BooleanVar()
        tk.Checkbutton(self.master, text="Enable LMS Filter", variable=self.lms_var, command=self.update_noise_setting).pack(anchor="w")
        self.lms_var.set(self.view_model.lms_enabled)

        # Apply Button
        self.apply_button = tk.Button(self.master, text="Apply Filters", command=self.apply_filters)
        self.apply_button.pack(pady=20)

        self.highcut_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.lowcut_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.amplitude_cut_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.hum_freq_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())
        self.q_factor_slider.bind("<ButtonRelease-1>", lambda event: self.update_noise_setting())

    def on_filter_change(self):
        self.view_model.update_model_from_view()

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