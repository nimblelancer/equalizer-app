import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
import time

class AudioGraphView2:
    def __init__(self, root, view_model):
        
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Tạo một frame chứa các button
        self.config_frame = tk.Frame(self.frame)
        self.config_frame.pack(pady=20)

        # Checkbutton để bật/tắt đồ thị
        self.show_graph_var = tk.IntVar()
        self.show_graph_checkbox = tk.Checkbutton(self.config_frame, text="Show Graph", variable=self.show_graph_var, command=self.show_graph)
        self.show_graph_var.set(1)
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

        # Vùng để hiển thị đồ thị
        self.canvas_frame = tk.Frame(self.frame)
        self.canvas_frame.pack()
        self.canvas = None
        self.g1 = None  # Đồ thị biên độ theo thời gian
        self.g2 = None  # Đồ thị phổ tần số của dữ liệu âm thanh
        self.g3 = None  # Đồ thị phổ tần số của dữ liệu đã lọc

        self.view_model = view_model
        self.view_model.add_view_listener(self)

        # Khởi tạo các biến cần thiết
        self.buffer_size = 1024 * 10
        self.audio_data_buffer = []  # Dữ liệu âm thanh tích lũy
        self.filtered_data_buffer = []  # Dữ liệu âm thanh tích lũy
        self.index = 0  # Chỉ số theo dõi vị trí trong âm thanh
        self.is_playing = False  # Biến điều khiển quá trình phát âm thanh
        self.update_interval = 0.05  # Khoảng thời gian giữa các lần cập nhật đồ thị (50ms)
        self.last_update_time = time.time()  # Thời gian của lần cập nhật cuối cùng

        self.framerate = 44100  # Framerate 44100 Hz

    def show_graph(self):
        self.view_model.toggle_graph(self.show_graph_var.get())
        if self.show_graph_var.get():
            if self.canvas is None:
                fig, axs = plt.subplots(2, 1, figsize=(10, 9))

                # Tạo đồ thị biên độ theo thời gian (g1)
                self.g1, = axs[0].plot([], [], label='Audio Signal', color='b')
                axs[0].set_xlim(0, self.buffer_size)
                axs[0].set_ylim(-1, 1)
                axs[0].set_title("Audio Signal - Time Domain")
                axs[0].set_xlabel("Samples")
                axs[0].set_ylabel("Amplitude")

                # Tạo đồ thị phổ tần số (g2 cho audio_data và g3 cho filtered_data)
                self.g2, = axs[1].plot([], [], label='Audio Signal Spectrum', color='b')
                self.g3, = axs[1].plot([], [], label='Filtered Signal Spectrum', color='r')
                axs[1].set_xlim(0, self.framerate // 2)  # Xem phổ tần số từ 0 đến Nyquist frequency
                axs[1].set_ylim(0, 1)  # Quy mô phổ tần số
                axs[1].set_title("Frequency Spectrum")
                axs[1].set_xlabel("Frequency (Hz)")
                axs[1].set_ylabel("Magnitude")
                axs[1].legend()

                # Đặt đồ thị vào Tkinter canvas
                for widget in self.canvas_frame.winfo_children():
                    widget.destroy()  # Xóa các đồ thị cũ

                self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack()

    def plot_spectrum(self, audio_data, filtered_data):
        """Vẽ đồ thị phổ tần số của dữ liệu âm thanh và đã lọc"""
        if self.g1 is None or self.g2 is None or self.g3 is None:
            print("Error: One of the plot objects (g1, g2, g3) is None, make sure show_graph is called first.")
            return

        if self.canvas is None:
            print("Error: canvas is None, make sure show_graph is called first.")
            return

        # Cập nhật đồ thị biên độ theo thời gian (g1)
        self.g1.set_ydata(audio_data)  # Cập nhật dữ liệu biên độ theo thời gian
        self.g1.set_xdata(np.arange(len(audio_data)))  # Cập nhật trục x

        # Tính toán FFT của audio_data và filtered_data
        N = len(audio_data)
        freqs = fftfreq(N, d=1 / self.framerate)[:N // 2]  # Chỉ lấy phần dương của phổ tần số
        audio_fft = np.abs(fft(audio_data))[:N // 2]
        filtered_fft = np.abs(fft(filtered_data))[:N // 2]

        # Cập nhật đồ thị phổ tần số (g2 cho audio_data và g3 cho filtered_data)
        self.g2.set_xdata(freqs)
        self.g2.set_ydata(audio_fft)  # Cập nhật phổ tần số của audio_data

        self.g3.set_xdata(freqs)
        self.g3.set_ydata(filtered_fft)  # Cập nhật phổ tần số của filtered_data

        # Cập nhật đồ thị
        self.canvas.draw()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def update_view(self, event_name, data):
        # Kiểm tra và điều chỉnh kích thước dữ liệu âm thanh
        audio_data = self.adjust_data_size(data.get("audio_data"))
        audio_data_normalized = self.normalize_audio_data(audio_data)
        filtered_data = self.adjust_data_size(data.get("filtered_data"))
        filtered_data_normalized = self.normalize_audio_data(filtered_data)

        # Thêm dữ liệu vào buffer
        self.audio_data_buffer.extend(audio_data_normalized)
        self.filtered_data_buffer.extend(filtered_data_normalized)

        # Nếu buffer đủ lớn (ví dụ 2048 mẫu), vẽ đồ thị
        if len(self.audio_data_buffer) >= self.buffer_size:
            # Lấy phần dữ liệu từ buffer và vẽ đồ thị
            audio_data_to_plot = self.audio_data_buffer[:self.buffer_size]
            filtered_data_to_plot = self.filtered_data_buffer[:self.buffer_size]
            self.plot_spectrum(audio_data_to_plot, filtered_data_to_plot)

            # Xóa phần dữ liệu đã vẽ khỏi buffer
            self.audio_data_buffer = self.audio_data_buffer[self.buffer_size:]
            self.filtered_data_buffer = self.filtered_data_buffer[self.buffer_size:]

    def adjust_data_size(self, audio_data):
        """Điều chỉnh kích thước dữ liệu âm thanh sao cho đồng nhất"""
        target_size = 1024
        if len(audio_data) < target_size:
            audio_data = np.pad(audio_data, (0, target_size - len(audio_data)), 'constant', constant_values=0)
        elif len(audio_data) > target_size:
            audio_data = audio_data[:target_size]
        return audio_data
    
    def normalize_audio_data(self, audio_data):
        """Chuẩn hóa dữ liệu âm thanh vào phạm vi [-1, 1]"""
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val
        return audio_data
