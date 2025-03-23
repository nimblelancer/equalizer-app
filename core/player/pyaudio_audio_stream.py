import pyaudio
from core.player.base_audio_stream import G2AudioStream

class PyAudioStreamWrapper(G2AudioStream):
    def __init__(self, channels, rate, input=True, output=True, frames_per_buffer=1024):
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = self.pyaudio_instance.open(format=pyaudio.paInt16,
                                                 channels=channels,
                                                 rate=rate,
                                                 input=input,
                                                 output=output,
                                                 frames_per_buffer=frames_per_buffer)

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
        self.stream.write(data)

    def read(self, chunk_size):
        """Đọc dữ liệu từ stream"""
        return self.stream.read(chunk_size)

    def close(self):
        """Đóng stream và kết thúc PyAudio"""
        self.stream.stop_stream()
        self.stream.close()
        self.pyaudio_instance.terminate()
