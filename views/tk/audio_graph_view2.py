import tkinter as tk
# import numpy as np
import time
from views.tk.audio_spectrum_graphview import AudioSpectrumGraphView
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel

class AudioGraphView2:
    def __init__(self, root, view_model:AudioGraphViewModel):
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Tạo một frame chứa các button
        self.config_frame = tk.Frame(self.frame)
        self.config_frame.pack(pady=20)

        self.view_model = view_model
        self.view_model.add_view_listener(self)

        # Checkbutton để bật/tắt đồ thị
        self.show_graph_var = tk.IntVar()
        self.show_graph_checkbox = tk.Checkbutton(self.config_frame, text="Show Graph", variable=self.show_graph_var, command=self.show_graph)
        self.show_graph_var.set(self.view_model.show_graph)
        self.show_graph_checkbox.pack(side=tk.LEFT, padx=5)

        # Tạo instance của GraphView
        self.graph_view = AudioSpectrumGraphView(self.frame)

        # Nhập tần số thấp nhất và cao nhất để giới hạn trục tần số
        self.freq_low_label = tk.Label(self.config_frame, text="Low Frequency (Hz):")
        self.freq_low_label.pack(side=tk.LEFT, padx=5)
        self.freq_low_entry = tk.Entry(self.config_frame)
        self.freq_low_entry.pack(side=tk.LEFT, padx=5)
        self.freq_low_entry.insert(tk.END, "20")  # Giá trị mặc định là 20Hz

        self.freq_high_label = tk.Label(self.config_frame, text="High Frequency (Hz):")
        self.freq_high_label.pack(side=tk.LEFT, padx=5)
        self.freq_high_entry = tk.Entry(self.config_frame)
        self.freq_high_entry.pack(side=tk.LEFT, padx=5)
        self.freq_high_entry.insert(tk.END, "5000")  # Giá trị mặc định là 5000Hz

    def show_graph(self):
        self.view_model.toggle_graph(self.show_graph_var.get())

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def update_view(self, event_name, data):
        if event_name == "audio_chunk_changed":
            # Kiểm tra và điều chỉnh kích thước dữ liệu âm thanh
            self.graph_view.plot_spectrum(data.get("audio_data"), data.get("filtered_data"))