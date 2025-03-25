import threading
import numpy as np
from core.player.base_audio_stream import G2AudioStream
from models.base_model import G2BaseModel
import wave
from core.player.equalizer_service2 import EqualizerService2
from typing import Type
from config_manager import ConfigManager

# AUDIO_FS = 44100
# AUDIO_CHUNK = 1024
# VOICE_FS = 44100
# VOICE_FPB = 1024
# VOICE_CHUNK = 1024

class AudioPlayerState:
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    RECORDING = 3

class AudioPlayerModel(G2BaseModel):
    def __init__(self, audio_stream_class: Type[G2AudioStream], eq_service: EqualizerService2, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
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
        self.fs = 44100

        self.show_graph = False
    
    def on_close(self):
        """Hàm xử lý khi đóng ứng dụng hoặc đối tượng AudioPlayerModel2."""
        print("Closing AudioPlayerModel2...")

        # Dừng audio playback nếu đang chơi
        if self.get_state() == AudioPlayerState.PLAYING:
            self.stop_audio()

        # Dừng ghi âm nếu đang ghi âm
        if self.get_state() == AudioPlayerState.RECORDING:
            self.set_state(AudioPlayerState.STOPPED)
            self.stopped_event.set()

        # Đảm bảo rằng các thread được dừng
        if self.audio_thread_instance is not None and self.audio_thread_instance.is_alive():
            print("Waiting for audio thread to finish...")
            self.audio_thread_instance.join()

        # Đóng audio stream nếu cần thiết
        if self.audio_stream is not None:
            self.audio_stream.close()

        super().on_close()

        print("AudioPlayerModel2 closed.")

    def set_state(self, state):
        """Cập nhật trạng thái của audio"""
        self.state = state
        self.notify_queued("player_state_changed", {
                    "state": self.state
                })

    def get_state(self):
        """Lấy trạng thái hiện tại"""
        return self.state
    
    def set_audio_file(self, file_path):
        self.selected_file = file_path

    def play_audio(self):
        """Bắt đầu phát âm thanh từ file"""
        if not self.selected_file:
            print("No audio file selected!")
            return
        wf = wave.open(self.selected_file, 'rb')
        self.fs = wf.getframerate()
        self.eq_service.reset_audio(fs=self.fs)

        self.notify_queued("audio_stream_changed", {
                    "framerate": self.fs
                })
        
        self.audio_stream = self.audio_stream_class(channels=wf.getnchannels(), 
                                                    rate=self.fs, 
                                                    frames_per_buffer=self.config_manager.getint('general', 'audio_fpb'))
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

        self.config_manager.reload_config()

        audio_chunk_size = self.config_manager.getint('general', 'audio_chunk_size')
        overlap_size = self.config_manager.getint('general', 'overlap_size')
        fade_size = self.config_manager.getint('general', 'fade_size')
        window_size = self.config_manager.getint('general', 'window_size')
        apply_soft_cliping = self.config_manager.getint('general', 'apply_soft_cliping')
        threshole_clip_small = self.config_manager.getfloat('general', 'threshole_clip_small')
        apply_cross_fade = self.config_manager.getfloat('general', 'apply_cross_fade')

        data = wf.readframes(audio_chunk_size)
        # overlap = np.zeros(overlap_size, dtype=np.int16)  # Khởi tạo overlap
        previous_chunk = None

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

            data = wf.readframes(audio_chunk_size)

        # self.stop_audio()
        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()  # Set event để thông báo cho thread dừng
        
        with self.lock:
            self.audio_stream.close()

    def start_voice(self):
        """Bắt đầu ghi âm từ microphone"""
        self.set_state(AudioPlayerState.RECORDING)
        self.fs = self.config_manager.getint('general', 'voice_fs')
        self.audio_stream = self.audio_stream_class(channels=1,
                                                 rate=self.fs,
                                                 input=True,
                                                 frames_per_buffer=self.config_manager.getint('general', 'voice_fpb'))
        
        
        self.eq_service.reset_audio(fs=self.fs)

        self._start_micro_thread()

    def _start_micro_thread(self):
        """Bắt đầu thread phát âm thanh"""
        self.audio_thread_instance = threading.Thread(target=self._micro_thread)
        self.audio_thread_instance.start()

    def _micro_thread(self):
        """Ghi âm từ micro và phát lại"""
        self.config_manager.reload_config()
        voice_chunk_size = self.config_manager.getint('general', 'voice_chunk_size')
        threshole_clip_small = self.config_manager.getfloat('general', 'threshole_clip_small')
        output_file = 'recorded_audio.wav'
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(1)  # Số kênh âm thanh (1 cho mono, 2 cho stereo)
            wf.setsampwidth(2)  # Chiều rộng mẫu (2 byte cho int16)
            wf.setframerate(self.fs)  # Tốc độ mẫu (44100 Hz)
            while self.get_state() == AudioPlayerState.RECORDING:
                data = self.audio_stream.read(voice_chunk_size)
                audio_data = np.frombuffer(data, dtype=np.int16)

                # audio_data = self.noise_reduction(audio_data)

                # Áp dụng EQ filter nếu cần
                # filtered_data = self.eq_service.equalize(audio_data, self.eq_apply, self.gains,
                #                                          self.lowcut_freq, self.highcut_freq, fs=44100)
                filtered_data = self.eq_service.equalize(audio_data)

                filtered_data = np.clip(filtered_data * self.volume, -32768, 32767)
                # filtered_data = np.clip(audio_data * self.volume, -32768, 32767)
                if threshole_clip_small > 0:
                    filtered_data = self.eq_service.clip_small_amplitudes(filtered_data, threshole_clip_small)

                if self.show_graph:
                    self.notify_queued("audio_chunk_changed", {
                        "audio_data": audio_data,
                        "filtered_data": filtered_data
                    })

                # Gửi dữ liệu đã lọc đến audio stream để phát lại
                with self.lock:
                    self.audio_stream.write(filtered_data.astype(np.int16).tobytes())
                wf.writeframes(filtered_data.astype(np.int16).tobytes())

        # Khi dừng ghi âm, xử lý cuối cùng
        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()