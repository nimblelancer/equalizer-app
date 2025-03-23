import ttkbootstrap as ttk
import matplotlib.pyplot as plt
import numpy as np
import time
from views.ttkbootstrap.audio_spectrum_graphview import AudioSpectrumGraphView

class AudioGraphView2:
    def __init__(self, root, view_model):
        self.style = ttk.Style()  # Lấy style từ ttkbootstrap

        self.frame = ttk.Frame(root)
        self.frame.pack()

        self.config_frame = ttk.Frame(self.frame)
        self.config_frame.pack(pady=20)

        # Lấy màu từ theme hiện tại
        bg_color = self.style.lookup("TFrame", "background")
        fg_color = self.style.lookup("TLabel", "foreground")

        # Truyền style cho AudioSpectrumGraphView
        self.graph_view = AudioSpectrumGraphView(
            self.frame,
            theme_colors={
                "bg": bg_color or "#2e2e2e",
                "fg": fg_color or "white",
                "line1": "#00BFFF",
                "line2": "#FF4500"
            }
        )

        self.view_model = view_model
        # Mặc định hiển thị đồ thị
        self.view_model.toggle_graph(True)
        self.graph_view.show_graph()
        
        # Nhập tần số thấp nhất và cao nhất để giới hạn trục tần số
        self.freq_low_label = ttk.Label(self.config_frame, text="Low Frequency (Hz):")
        self.freq_low_label.pack(side=ttk.LEFT, padx=5)
        self.freq_low_entry = ttk.Entry(self.config_frame, width=10)
        self.freq_low_entry.pack(side=ttk.LEFT, padx=5)
        self.freq_low_entry.insert(ttk.END, "20")  # Giá trị mặc định là 20Hz

        self.freq_high_label = ttk.Label(self.config_frame, text="High Frequency (Hz):")
        self.freq_high_label.pack(side=ttk.LEFT, padx=5)
        self.freq_high_entry = ttk.Entry(self.config_frame, width=10)
        self.freq_high_entry.pack(side=ttk.LEFT, padx=5)
        self.freq_high_entry.insert(ttk.END, "5000")  # Giá trị mặc định là 5000Hz

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

    def plot_spectrum(self, audio_data, filtered_data):
        """Vẽ đồ thị phổ tần số của dữ liệu âm thanh và đã lọc"""
        self.graph_view.plot_spectrum(audio_data, filtered_data)

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
