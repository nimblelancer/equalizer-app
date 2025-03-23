import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from audio_graph_viewmodel import AudioGraphViewModel
import time
import numpy as np

class AudioGraphView:
    def __init__(self, root, view_model: AudioGraphViewModel):
        print('view 1')
        
        self.frame = tk.Frame(root)
        self.frame.pack()

        # Tạo một frame chứa các button
        self.config_frame = tk.Frame(self.frame)
        self.config_frame.pack(pady=20)

        # # Nút để áp dụng bộ lọc và vẽ đồ thị
        self.apply_button = tk.Button(self.config_frame, text="Apply Filter", command=self.apply_filter)
        self.apply_button.pack(side=tk.LEFT, padx=5)

        # Checkbutton để bật/tắt đồ thị
        self.show_graph_var = tk.IntVar()
        self.show_graph_checkbox = tk.Checkbutton(self.config_frame, text="Show Graph", variable=self.show_graph_var, command=self.show_graph)
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
        self.freq_high_entry.insert(tk.END, "5000")  # Giá trị mặc định là 20000Hz

        # Vùng để hiển thị đồ thị
        self.canvas_frame = tk.Frame(self.frame)
        self.canvas_frame.pack()
        self.canvas = None
        self.g1 = None
        self.g2 = None
        self.g3 = None
        self.g4 = None

        self.view_model = view_model

        self.view_model.add_view_listener(self)

        self.last_update_time = 0  # Thời gian của lần cập nhật cuối cùng
        self.update_interval = 3  # Thời gian giữa các lần cập nhật (3 giây)
        self.audio_data_buffer = []  # Dữ liệu âm thanh tích lũy
        self.filtered_data_buffer = []  # Dữ liệu âm thanh đã lọc tích lũy

    def show_graph(self):
        self.view_model.toggle_graph(self.show_graph_var.get())
        if self.show_graph_var.get():
            if self.canvas is None:
                """Vẽ đồ thị tần số trước và sau khi lọc"""
                fig, axs = plt.subplots(3, 1, figsize=(10, 9))

                # Đồ thị của dữ liệu gốc
                self.g1, = axs[0].plot(np.zeros(2048), label="Original Audio")
                axs[0].set_title("Original Audio Spectrum")
                axs[0].set_xlabel('Sample Index')
                axs[0].set_ylabel('Amplitude')
                axs[0].grid(True)

                # Đồ thị của dữ liệu đã lọc
                self.g2, = axs[1].plot(np.zeros(1024), label="Filtered Audio", color="r")
                axs[1].set_title("Filtered Audio Spectrum")
                axs[1].set_xlabel('Sample Index')
                axs[1].set_ylabel('Amplitude')
                axs[1].grid(True)

                self.g3, = axs[2].plot(np.arange(0, 2048), np.zeros(2048), label="Original Audio Frequency Response")
                self.g4, = axs[2].plot(np.arange(0, 2048), np.zeros(2048), label="Filtered Audio Frequency Response", color="r")
                axs[2].set_title("Frequency Response (FFT)")
                axs[2].set_xlabel('Frequency (Hz)')
                axs[2].set_ylabel('Amplitude')
                axs[2].grid(True)
                axs[2].legend()

                # Đặt đồ thị vào Tkinter canvas
                for widget in self.canvas_frame.winfo_children():
                    widget.destroy()  # Xóa các đồ thị cũ

                self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack()

                print(f"Number of open figures: {len(plt.get_fignums())}")

                

                # Đóng figure để giải phóng bộ nhớ
                # plt.close(fig)

    def apply_filter(self):
        """Áp dụng bộ lọc và cập nhật đồ thị"""
        # Lấy dữ liệu từ ViewModel
        original_audio_data, filtered_audio_data = self.view_model.get_audio_data()

        # Vẽ đồ thị
        self.plot_spectrum(original_audio_data, filtered_audio_data)

    def plot_spectrum(self, original_audio_data, filtered_audio_data):
        # self.g1.set_ydata(original_audio_data)
        # Lấy giá trị tần số thấp nhất và cao nhất từ ô nhập
        freq_low = float(self.freq_low_entry.get())
        freq_high = float(self.freq_high_entry.get())

        n = 2048  # Giả sử bạn muốn chiều dài dữ liệu là 1024
        original_audio_data = np.pad(original_audio_data, (0, max(0, n - len(original_audio_data))), 'constant')
        filtered_audio_data = np.pad(filtered_audio_data, (0, max(0, n - len(filtered_audio_data))), 'constant')


        # Đồ thị đáp ứng tần số (FFT của tín hiệu gốc và tín hiệu đã lọc)
        # Tính toán FFT của tín hiệu gốc và tín hiệu đã lọc
        original_fft = np.fft.fft(original_audio_data)
        filtered_fft = np.fft.fft(filtered_audio_data)

        # Lấy tần số (x-axis cho đồ thị đáp ứng tần số)
        sample_rate = 44100  # Giả sử sample rate là 44100 Hz
        freqs = np.fft.fftfreq(len(original_audio_data), 1 / sample_rate)
        positive_freqs = freqs[:len(freqs) // 2]  # Chỉ lấy nửa tần số dương

        # Lấy biên độ của FFT (chỉ lấy nửa đầu, vì FFT là đối xứng)
        original_amplitude = np.abs(original_fft[:len(original_fft) // 2])
        filtered_amplitude = np.abs(filtered_fft[:len(filtered_fft) // 2])

        # Lọc dữ liệu để chỉ hiển thị trong phạm vi tần số đã nhập
        mask = (positive_freqs >= freq_low) & (positive_freqs <= freq_high)
        positive_freqs = positive_freqs[mask]
        original_amplitude = original_amplitude[mask]
        filtered_amplitude = filtered_amplitude[mask]

        # self.g3.set_xdata(positive_freqs)
        self.g3.set_ydata(original_audio_data)
        # self.g4.set_xdata(positive_freqs)
        self.g4.set_ydata(filtered_amplitude)

        self.canvas.draw()
        self.canvas.flush_events()

        # self.frame.master.after(50, self.plot_spectrum, original_audio_data, filtered_audio_data)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def update_view(self, event_name, data):
        self.plot_spectrum(data.get("audio_data"), data.get("filtered_data"))