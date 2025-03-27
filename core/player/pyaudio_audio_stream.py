import pyaudio
from core.player.base_audio_stream import G2AudioStream
import time

class PyAudioStreamWrapper(G2AudioStream):
    def __init__(self, channels, rate, input=True, output=True, frames_per_buffer=1024):
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = self.pyaudio_instance.open(format=pyaudio.paInt16,
                                                 channels=channels,
                                                 rate=rate,
                                                 input=input,
                                                 output=output,
                                                 frames_per_buffer=frames_per_buffer)
        self.current_frame = 0

    def start_stream(self):
        """Bắt đầu stream âm thanh"""
        if not self.stream.is_active():
            self.stream.start_stream()

    def stop_stream(self):
        """Dừng stream âm thanh"""
        if self.stream.is_active():
            self.stream.stop_stream()

    def write(self, data):
        """Viết dữ liệu vào stream"""
        start_time = self.stream.get_time()  # Lấy thời gian trước khi phát
        self.stream.write(data)

        elapsed_time = self.stream.get_time() - start_time  # Tính thời gian thực sự phát
        self.current_frame += int(elapsed_time * self.stream._rate)  # Đồng bộ số frame

    def get_position(self):
        """Trả về vị trí frame hiện tại"""
        return self.current_frame

    def read(self, chunk_size, exception_on_overflow=False):
        """Đọc dữ liệu từ stream"""
        return self.stream.read(chunk_size, exception_on_overflow=exception_on_overflow)

    def close(self):
        """Đóng stream và kết thúc PyAudio"""
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio_instance.terminate()
