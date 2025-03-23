import threading
import numpy as np
from core.player.base_audio_stream import G2AudioStream
from models.base_model import G2BaseModel
import wave
from core.player.equalizer_service2 import EqualizerService2
from typing import Type

class AudioPlayerState:
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    RECORDING = 3

class AudioPlayerModel(G2BaseModel):
    def __init__(self, audio_stream_class: Type[G2AudioStream], eq_service: EqualizerService2):
        super().__init__()

        self.state = AudioPlayerState.STOPPED
        self.audio_stream = None
        self.audio_stream_class = audio_stream_class
        self.eq_service = eq_service
        self.selected_file = "data/audio.wav"
        self.audio_thread_instance = None
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.stopped_event = threading.Event()  # Event để dừng thread

        self.volume = 1

        self.eq_apply = False

        # self.gains = {
        #     'Bass': 1,
        #     'Mid-bass': 1,
        #     'Midrange': 1,
        #     'Upper midrange': 1,
        #     'Treble': 1
        # }

        self.lowcut_freq = 0
        self.highcut_freq = 0

        self.show_graph = False
    
    def set_eq_applied(self, eq_apply, gains, low_cut, high_cut):
        self.eq_apply = eq_apply
        self.gains = gains
        self.lowcut_freq = low_cut
        self.highcut_freq = high_cut
        
        self.eq_service.reset_eq()

    def set_state(self, state):
        """Cập nhật trạng thái của audio"""
        self.state = state

    def get_state(self):
        """Lấy trạng thái hiện tại"""
        return self.state

    def play_audio(self):
        """Bắt đầu phát âm thanh từ file"""
        if not self.selected_file:
            print("No audio file selected!")
            return

        wf = wave.open(self.selected_file, 'rb')
        print("framerate:", wf.getframerate())
        self.audio_stream = self.audio_stream_class(channels=wf.getnchannels(), rate=wf.getframerate())
        self.set_state(AudioPlayerState.PLAYING)
        self.stopped_event.clear()  # Đảm bảo rằng event không bị set khi bắt đầu lại
        self._start_audio_thread(wf)

        thread_count = threading.active_count()
        print(f"Number of threads in the current process: {thread_count}")

    def stop_audio(self):
        """Dừng âm thanh"""
        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()  # Set event để thông báo cho thread dừng
        if self.audio_thread_instance is not None:
            self.audio_thread_instance.join()

    def pause_audio(self):
        """Tạm dừng âm thanh"""
        self.set_state(AudioPlayerState.PAUSED)
        if self.audio_thread_instance:
            with self.lock:  # Locking the stream to prevent race conditions
                self.audio_stream.stop_stream()
        self.event.clear()  # Đưa event về trạng thái "clear" (tạm dừng)

    def unpause_audio(self):
        """Tiếp tục phát âm thanh"""
        self.set_state(AudioPlayerState.PLAYING)
        with self.lock:  # Locking the stream to prevent race conditions
            self.audio_stream.start_stream()
        self.event.set()  # Đưa event về trạng thái "set" (tiếp tục)

    def _start_audio_thread(self, wf):
        """Bắt đầu thread phát âm thanh"""
        self.audio_thread_instance = threading.Thread(target=self._audio_thread, args=(wf,))
        self.audio_thread_instance.start()

    def _audio_thread(self, wf):

        if self.state == AudioPlayerState.PAUSED:
            self.event.wait()  # Dừng thread khi paused

        chunk = 1024
        data = wf.readframes(chunk)

        # print(self.eq_apply, self.bands, self.lowcut_freq, self.highcut_freq)

        while data:
            # Check if the audio is still in PLAYING state
            if self.get_state() != AudioPlayerState.PLAYING:
                break  # Exit the loop if audio is no longer playing

            audio_data = np.frombuffer(data, dtype=np.int16)
            # filtered_data = audio_data

            # Áp dụng bộ lọc cho dữ liệu âm thanh
            filtered_data = self.eq_service.equalize(audio_data)

            # Điều chỉnh âm lượng của dữ liệu âm thanh trước khi ghi vào stream
            filtered_data = np.clip(filtered_data * self.volume, -32768, 32767)  # Áp dụng volume và giới hạn giá trị âm thanh

            if self.show_graph:
                self.notify_queued("audio_chunk_changed", {
                    "audio_data": audio_data,
                    "filtered_data": filtered_data
                })

            # Check if the audio is still in PLAYING state
            if self.get_state() != AudioPlayerState.PLAYING:
                break  # Exit the loop if audio is no longer playing

            with self.lock:  # Locking the stream to prevent race conditions while writing
                # Check if the audio is still in PLAYING state
                if self.get_state() != AudioPlayerState.PLAYING:
                    break  # Exit the loop if audio is no longer playing

                self.audio_stream.write(filtered_data.astype(np.int16).tobytes())

            # Check if the audio is still in PLAYING state
            if self.get_state() != AudioPlayerState.PLAYING:
                break  # Exit the loop if audio is no longer playing

            data = wf.readframes(chunk)

        # self.stop_audio()
        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()  # Set event để thông báo cho thread dừng
        
        with self.lock:
            self.audio_stream.close()

    def start_voice(self):
        """Bắt đầu ghi âm từ microphone"""
        self.set_state(AudioPlayerState.RECORDING)
        self.audio_stream = self.audio_stream_class(channels=1,
                                                 rate=44100,
                                                 input=True,
                                                 frames_per_buffer=1024)

        self._start_micro_thread()

    def _start_micro_thread(self):
        """Bắt đầu thread phát âm thanh"""
        self.audio_thread_instance = threading.Thread(target=self._micro_thread)
        self.audio_thread_instance.start()

    def _micro_thread(self):
        """Ghi âm từ micro và phát lại"""
        audio_data_buffer = []
        while self.get_state() == AudioPlayerState.RECORDING:
            data = self.audio_stream.read(1024)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Áp dụng EQ filter nếu cần
            filtered_data = self.eq_service.equalize(audio_data, self.eq_apply, self.gains,
                                                     self.lowcut_freq, self.highcut_freq, fs=44100)

            filtered_data = np.clip(filtered_data * self.volume, -32768, 32767)

            if self.show_graph:
                self.notify_queued("audio_chunk_changed", {
                    "audio_data": audio_data,
                    "filtered_data": filtered_data
                })

            # Gửi dữ liệu đã lọc đến audio stream để phát lại
            with self.lock:
                self.audio_stream.write(filtered_data.astype(np.int16).tobytes())

            # Thêm dữ liệu vào buffer nếu cần xử lý thêm
            audio_data_buffer.append(filtered_data)

        # Khi dừng ghi âm, xử lý cuối cùng
        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()