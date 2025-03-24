import numpy as np
from scipy.signal import butter, lfilter
from viewmodels.base_viewmodel import G2BaseViewModel
from models.audio_player_model import AudioPlayerModel
import time
import scipy.signal as signal
from scipy.fft import fft

class AudioGraphViewModel(G2BaseViewModel):
    def __init__(self, model: AudioPlayerModel):
        super().__init__(model)
        self.model.add_listener("audio_chunk_changed", self)

        self.show_graph = self.model.show_graph

        self.audio_data = None
        self.filtered_data = None

        # Khởi tạo các biến cần thiết
        self.buffer_size = 1024 * 3
        self.audio_data_buffer = []  # Dữ liệu âm thanh tích lũy
        self.filtered_data_buffer = []  # Dữ liệu âm thanh tích lũy
        self.index = 0  # Chỉ số theo dõi vị trí trong âm thanh
        self.is_playing = False  # Biến điều khiển quá trình phát âm thanh
        self.update_interval = 0.05  # Khoảng thời gian giữa các lần cập nhật đồ thị (50ms)
        self.last_update_time = time.time()  # Thời gian của lần cập nhật cuối cùng

        self.fs = 44100  # Framerate 44100 Hz

        # self.t = []


    def get_time_array(self, audio_data):
        """
        Trả về mảng thời gian tương ứng với dữ liệu âm thanh.
        """
        return np.linspace(0, len(audio_data) / self.fs, num=len(audio_data))


    def toggle_graph(self, is_show):
        self.show_graph = is_show
        self.model.show_graph = is_show

    # def update_audio_data(self, original_audio_data, filtered_audio_data):
    #     """Cập nhật dữ liệu âm thanh cho View"""
    #     self.original_audio_data = original_audio_data
    #     self.filtered_audio_data = filtered_audio_data

    # def butter_bandpass(self, lowcut, highcut, order=4):
    #     nyquist = 0.5 * 44100
    #     low = lowcut / nyquist
    #     high = highcut / nyquist
    #     b, a = butter(order, [low, high], btype='band')
    #     return b, a

    # def apply_filter(self, data, lowcut, highcut):
    #     b, a = self.butter_bandpass(lowcut, highcut)
    #     return lfilter(b, a, data)

    # def get_audio_data(self):
    #     t = np.linspace(0, 1, 44100)
    #     self.original_audio_data = np.sin(2 * np.pi * 100 * t) + np.sin(2 * np.pi * 500 * t)  # Sóng 100Hz và 500Hz
    #     self.filtered_audio_data = self.apply_filter(self.original_audio_data, lowcut=150, highcut=1000)

    #     return self.original_audio_data, self.filtered_audio_data
    
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
    
    def calculate_spectrogram(self, data):
        """
        Tính toán spectrogram từ tín hiệu âm thanh.
        """
        # Ví dụ tính toán spectrogram
        data = np.array(data)
        f, t, Sxx = signal.spectrogram(data, fs=self.fs)
        return Sxx

    def calculate_frequency_spectrum(self, data):
        """
        Tính toán phổ tần số từ tín hiệu âm thanh.
        """
        N = len(data)
        T = 1.0 / self.fs
        x = np.linspace(0.0, N * T, N, endpoint=False)
        yf = fft(data)
        xf = np.fft.fftfreq(N, T)

        # Lấy nửa đầu của phổ (tần số dương)
        xf = xf[:N // 2]
        yf = yf[:N // 2]
        amplitude = np.abs(yf)

        return amplitude, xf

    def calculate_volume_level(self, data):
        """
        Tính toán mức âm lượng từ tín hiệu âm thanh.
        """
        return np.abs(data)  # Hoặc sử dụng một công thức tính âm lượng khác

    def calculate_frequency_bands(self, spectrum, xf):
        """
        Tính toán các dải tần số từ tín hiệu âm thanh.
        """
        # spectrum = self.calculate_frequency_spectrum(data)
        xf = np.array(xf)
        spectrum = np.array(spectrum)

        bands = {
            'bass': np.sum(spectrum[(xf >= 20) & (xf <= 150)]),  # Bass: 20Hz - 150Hz
            'mid_bass': np.sum(spectrum[(xf >= 150) & (xf <= 500)]),  # Mid-bass: 150Hz - 500Hz
            'midrange': np.sum(spectrum[(xf >= 500) & (xf <= 2000)]),  # Midrange: 500Hz - 2kHz
            'upper_mid': np.sum(spectrum[(xf >= 2000) & (xf <= 4000)]),  # Upper Mid: 2kHz - 4kHz
            'treble': np.sum(spectrum[(xf >= 4000) & (xf <= 20000)])  # Treble: 4kHz - 20kHz
        }
        return bands

    def calculate_fft(self, spectrum):
        """
        Tính toán FFT của tín hiệu âm thanh.
        """
        # spectrum = self.calculate_frequency_spectrum(data)
        return np.log(spectrum)

    def calculate_frequency_response(self, data):
        """
        Tính toán đáp ứng tần số (ví dụ: hệ thống lọc).
        """
        frequencies = np.logspace(np.log10(20), np.log10(20000), num=1000)
        response = 1 / (1 + 1j * frequencies / 1000)  # Giả sử là hệ thống lọc thông thấp
        return response
    
    def on_notify(self, event_name, data):
        if event_name == "audio_chunk_changed":
            # print("audio_chunk_changed in audio_graph_viewmodel")

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
                # audio_data_to_plot = self.audio_data_buffer[:self.buffer_size]
                # filtered_data_to_plot = self.filtered_data_buffer[:self.buffer_size]
                
                # self.plot_spectrum(audio_data_to_plot, filtered_data_to_plot)
                self.audio_data = np.copy(self.audio_data_buffer[:self.buffer_size])
                self.filtered_data = np.copy(self.filtered_data_buffer[:self.buffer_size])

                self.original_t = self.get_time_array(self.audio_data)
                self.filtered_t = self.get_time_array(self.filtered_data)

                self.original_spectrogram = self.calculate_spectrogram(self.audio_data)
                self.filtered_spectrogram = self.calculate_spectrogram(self.filtered_data)
                self.original_freq_spectrum, self.original_xf = self.calculate_frequency_spectrum(self.audio_data)
                self.filtered_freq_spectrum, self.filtered_xf = self.calculate_frequency_spectrum(self.filtered_data)
                self.original_volume_level = self.calculate_volume_level(self.audio_data)
                self.filtered_volume_level = self.calculate_volume_level(self.filtered_data)
                self.original_freq_bands = self.calculate_frequency_bands(self.original_freq_spectrum, self.original_xf)
                self.filtered_freq_bands  = self.calculate_frequency_bands(self.filtered_freq_spectrum, self.filtered_xf)
                self.original_fft = self.calculate_fft(self.original_freq_spectrum)
                self.filtered_fft = self.calculate_fft(self.filtered_freq_spectrum)
                self.original_freq_response = self.calculate_frequency_response(self.audio_data)
                self.filtered_freq_response = self.calculate_frequency_response(self.filtered_data)

                self.notify_view(event_name, None)

                # Xóa phần dữ liệu đã vẽ khỏi buffer
                self.audio_data_buffer = self.audio_data_buffer[self.buffer_size:]
                self.filtered_data_buffer = self.filtered_data_buffer[self.buffer_size:]
            # self.notify_view(event_name, None)
        else:
            super().notify_view(event_name, data)  # Gọi hàm super
