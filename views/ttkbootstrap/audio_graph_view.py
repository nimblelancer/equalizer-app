import tkinter as tk
# import numpy as np
import time
from viewmodels.audio_graph_viewmodel import AudioGraphViewModel
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from scipy.fft import fft
import scipy.signal as signal
import wave
from views.ttkbootstrap.graph_factory import GraphFactory

class AudioGraphView:
    def __init__(self, root, view_model: AudioGraphViewModel):
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)

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

        self.sample_rate = 44100

        self.figures = []
        self.graphs = []

        self.graph_original_waveform = None
        self.graph_filtered_waveform = None
        self.graph_original_spectrogram = None
        self.graph_filtered_spectrogram = None
        self.graph_original_freq_spectrum = None
        self.graph_filtered_freq_spectrum = None
        self.graph_original_vol_level = None
        self.graph_filtered_vol_level = None
        self.graph_original_freq_bar_chart = None
        self.graph_filtered_freq_bar_chart = None
        self.graph_original_fft = None
        self.graph_filtered_fft = None

        self.create_graphs(self.frame)

    def create_graphs(self, frame):
        # Tạo Canvas để chứa các đồ thị
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Thêm Scrollbar vào canvas
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Tạo một frame con để chứa các Canvas vẽ đồ thị
        graph_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=graph_frame, anchor="nw")

        # Số hàng và cột để chia đồ thị
        rows = 7  # Số loại đồ thị
        cols = 2  # Original và filtered data

        for i in range(7):
            # Tạo figure cho original và filtered data
            fig_original, ax_original = plt.subplots(figsize=(8, 4))
            fig_filtered, ax_filtered = plt.subplots(figsize=(8, 4))

            graph_factory_original = GraphFactory(ax_original)
            graph_factory_filtered = GraphFactory(ax_filtered)

            # Tạo các đồ thị tương ứng cho original và filtered data
            if i == 0:
                graph_factory_original.create_waveform()
                graph_factory_filtered.create_waveform()
            elif i == 1:
                graph_factory_original.create_spectrogram()
                graph_factory_filtered.create_spectrogram()
            elif i == 2:
                graph_factory_original.create_frequency_spectrum()
                graph_factory_filtered.create_frequency_spectrum()
            elif i == 3:
                graph_factory_original.create_volume_level()
                graph_factory_filtered.create_volume_level()
            elif i == 4:
                graph_factory_original.create_bar_chart()
                graph_factory_filtered.create_bar_chart()
            elif i == 5:
                graph_factory_original.create_fft()
                graph_factory_filtered.create_fft()
            elif i == 6:
                graph_factory_original.create_frequency_response()
                graph_factory_filtered.create_frequency_response()

            # Thêm đồ thị vào canvas
            canvas_widget_original = FigureCanvasTkAgg(fig_original, master=graph_frame)
            canvas_widget_filtered = FigureCanvasTkAgg(fig_filtered, master=graph_frame)
            canvas_widget_original.draw()
            canvas_widget_filtered.draw()

            # Tính toán row và column cho grid
            row = i
            col_original = 0
            col_filtered = 1

            # Chèn original data và filtered data vào grid
            canvas_widget_original.get_tk_widget().grid(row=row, column=col_original, padx=5, pady=5)
            canvas_widget_filtered.get_tk_widget().grid(row=row, column=col_filtered, padx=5, pady=5)

            self.figures.append((fig_original, fig_filtered))
            self.graphs.append((graph_factory_original, graph_factory_filtered))

        # Cập nhật kích thước của canvas sau khi tất cả các đồ thị đã được thêm vào
        graph_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def update_graphs(self):
        for i, (graph_factory_original, graph_factory_filtered) in enumerate(self.graphs):
            if i == 0:
                # continue
                self.update_graph(graph_factory_original, self.view_model.original_t, self.view_model.audio_data)
                self.update_graph(graph_factory_filtered, self.view_model.filtered_t, self.view_model.filtered_data)
            elif i == 1:
                # continue
                self.update_graph(graph_factory_original, self.view_model.original_t, self.view_model.original_spectrogram)
                self.update_graph(graph_factory_filtered, self.view_model.filtered_t, self.view_model.filtered_spectrogram)
            elif i == 2:
                # continue
                self.update_graph(graph_factory_original, self.view_model.original_xf, self.view_model.original_freq_spectrum)
                self.update_graph(graph_factory_filtered, self.view_model.filtered_xf, self.view_model.filtered_freq_spectrum)
            elif i == 3:
                # continue
                self.update_graph(graph_factory_original, self.view_model.original_t, self.view_model.original_volume_level)
                self.update_graph(graph_factory_filtered, self.view_model.filtered_t, self.view_model.filtered_volume_level)
            elif i == 4:
                # continue
                self.update_graph(graph_factory_original, self.view_model.original_freq_bands.keys(), self.view_model.original_freq_bands.values())
                self.update_graph(graph_factory_filtered, self.view_model.filtered_freq_bands.keys(), self.view_model.filtered_freq_bands.values())
            elif i == 5:
                # continue
                self.update_graph(graph_factory_original, self.view_model.original_xf, self.view_model.original_fft)
                self.update_graph(graph_factory_filtered, self.view_model.filtered_xf, self.view_model.filtered_fft)
            elif i == 6:
                continue
                self.update_graph(graph_factory_original, self.view_model.original_xf, self.view_model.original_freq_response)
                self.update_graph(graph_factory_filtered, self.view_model.filtered_xf, self.view_model.filtered_freq_response)


    def update_graph(self, graph_factory, new_x, new_y):
        if graph_factory.line is not None:
            new_y = np.asarray(new_y)
            graph_factory.line.set_xdata(new_x)
            graph_factory.line.set_ydata(new_y)

            # Cập nhật giới hạn trục x và y tự động
            # graph_factory.ax.relim()  # Cập nhật lại các giới hạn
            # graph_factory.ax.autoscale_view()  # Tự động điều chỉnh view để hiển thị dữ liệu mới

        elif graph_factory.im is not None:
            graph_factory.im.set_data(new_y)

            # Cập nhật lại giới hạn trục (trường hợp này có thể cần tùy chỉnh thêm)
            # graph_factory.ax.set_ylim([np.min(new_y), np.max(new_y)])

        elif graph_factory.bar is not None:
            # Cập nhật dữ liệu cho biểu đồ cột
            
            # graph_factory.ax.set_xticks(range(len(new_x)))  # Cập nhật lại vị trí của các cột trên trục x
            # graph_factory.ax.set_xticklabels(new_x)  # Cập nhật nhãn của trục x

            # new_y = np.asarray(new_y)
            for rect, height in zip(graph_factory.bar, new_y):
                rect.set_height(height)  # Cập nhật chiều cao của cột

        # Cập nhật giới hạn trục x và y tự động
        graph_factory.ax.relim()  # Cập nhật lại các giới hạn
        graph_factory.ax.autoscale_view()  # Tự động điều chỉnh view để hiển thị dữ liệu mới
        graph_factory.ax.figure.canvas.draw()



    def show_graph(self):
        self.view_model.toggle_graph(self.show_graph_var.get())

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def update_view(self, event_name, data):
        if event_name == "audio_chunk_changed":
            # Kiểm tra và điều chỉnh kích thước dữ liệu âm thanh
            # self.graph_view.plot_spectrum(data.get("audio_data"), data.get("filtered_data"))
            self.update_graphs()
