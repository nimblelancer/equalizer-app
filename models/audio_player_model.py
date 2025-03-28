import threading
import numpy as np
from core.player.base_audio_stream import G2AudioStream
from models.base_model import G2BaseModel
import wave
from core.player.equalizer_service2 import EqualizerService2
from core.player.noise_suppression_service import NoiseSuppressionService
from typing import Type
from scipy.signal import wiener, butter, filtfilt, get_window
from config_manager import ConfigManager
import librosa
import soundfile as sf
from pydub import AudioSegment
import os

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
    def __init__(self, 
            audio_stream_class: Type[G2AudioStream],
            eq_service: EqualizerService2,
            noise_service: NoiseSuppressionService,
            config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        self.state = AudioPlayerState.STOPPED
        self.audio_stream = None
        self.wave_file = None
        self.audio_stream_class = audio_stream_class
        self.eq_service = eq_service
        self.noise_service = noise_service
        self.selected_file = "data/audio.wav"
        self.audio_thread_instance = None
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.stopped_event = threading.Event()  # Event để dừng thread
        self.state_changed_callback = None

        self.volume = 1
        self.muted = False  # Trạng thái mute
        self.prev_volume = self.volume  # Lưu âm lượng trước khi mute
        self.fs = 44100

        self.show_graph = False
        self.current_frame = 0
    
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

    def set_state(self, new_state):
        """Cập nhật trạng thái của audio"""
        self.state = new_state
        if self.state_changed_callback:
            self.state_changed_callback(new_state)
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
        wf.rewind()
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
        self.stopped_event.set()  # Thông báo cho thread dừng

        self.current_frame = 0
        self.event.clear()

        if self.audio_thread_instance is not None:
            if self.audio_thread_instance.is_alive():  # Kiểm tra thread có đang chạy không
                self.audio_thread_instance.join(timeout=2)

    def pause_audio(self):
        """Tạm dừng hoặc tiếp tục phát âm thanh"""
        if self.state == AudioPlayerState.PLAYING:
            self.set_state(AudioPlayerState.PAUSED)
            with self.lock:
                self.audio_stream.stop_stream()
            self.event.clear()
            self.current_frame = self.audio_stream.get_position()  # Lưu vị trí hiện tại
        elif self.state == AudioPlayerState.PAUSED:
            self.unpause_audio()

    def unpause_audio(self):
        """Tiếp tục phát từ vị trí đã dừng"""
        if self.state == AudioPlayerState.PAUSED:
            self.set_state(AudioPlayerState.PLAYING)
            with self.lock:
                if not self.audio_stream.stream.is_active():  # Kiểm tra nếu stream đã đóng
                    self.audio_stream.start_stream()
            self.event.set()

    def _start_audio_thread(self, wf):
        """Bắt đầu thread phát âm thanh"""
        self.audio_thread_instance = threading.Thread(target=self._audio_thread, args=(wf,))
        self.audio_thread_instance.start()

    def _audio_thread(self, wf):
        """Thread xử lý phát âm thanh, hỗ trợ pause và tiếp tục từ vị trí dừng"""
        self.config_manager.reload_config()

        audio_chunk_size = self.config_manager.getint('general', 'audio_chunk_size')
        overlap_size = self.config_manager.getint('general', 'overlap_size')
        fade_size = self.config_manager.getint('general', 'fade_size')
        window_size = self.config_manager.getint('general', 'window_size')
        apply_soft_cliping = self.config_manager.getint('general', 'apply_soft_cliping')
        threshole_clip_small = self.config_manager.getfloat('general', 'threshole_clip_small')
        apply_cross_fade = self.config_manager.getfloat('general', 'apply_cross_fade')

        # Nếu đã pause trước đó, đặt lại vị trí đọc file
        if self.current_frame > 0:
            wf.setpos(self.current_frame)

        data = wf.readframes(audio_chunk_size)
        # overlap = np.zeros(overlap_size, dtype=np.int16)  # Khởi tạo overlap
        previous_chunk = None


        while self.get_state() != AudioPlayerState.STOPPED:
            if self.get_state() == AudioPlayerState.PAUSED:
                self.current_frame = wf.tell()  # Lưu lại vị trí frame khi pause
                self.event.wait()  # Chờ đến khi Unpause
                wf.setpos(self.current_frame)  # Quay lại vị trí đã dừng
                continue  # Tiếp tục phát từ vị trí đã dừng 
            
            if not data:
                break

            audio_data = np.frombuffer(data, dtype=np.int16)
            # filtered_data = audio_data

            filtered_data = self.noise_service.suppress_noise(audio_data)
            # Áp dụng bộ lọc cho dữ liệu âm thanh
            filtered_data = self.eq_service.equalize(filtered_data)

            # Điều chỉnh âm lượng của dữ liệu âm thanh trước khi ghi vào stream
            filtered_data = np.clip(filtered_data * self.volume, -32768, 32767)  # Áp dụng volume và giới hạn giá trị âm thanh

            if self.show_graph:
                self.notify_queued("audio_chunk_changed", {
                    "audio_data": audio_data,
                    "filtered_data": filtered_data
                })

            with self.lock:  # Locking the stream to prevent race conditions while writing
                # Check if the audio is still in PLAYING state
                if self.get_state() == AudioPlayerState.PLAYING:
                    self.audio_stream.write(filtered_data.astype(np.int16).tobytes())

            data = wf.readframes(audio_chunk_size)

        # Nếu phát hết file, đặt trạng thái về STOPPED
        if self.get_state() == AudioPlayerState.PLAYING:
            self.set_state(AudioPlayerState.STOPPED)
            self.stopped_event.set()
        
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
            while self.get_state() == AudioPlayerState.RECORDING and not self.stopped_event.is_set():
                try:
                    data = self.audio_stream.read(voice_chunk_size, exception_on_overflow=False)
                except Exception as e:
                    print(f"Error reading audio stream: {e}")
                    break

                audio_data = np.frombuffer(data, dtype=np.int16)

                # audio_data = self.noise_reduction(audio_data)
                filtered_data = self.noise_service.suppress_noise(audio_data)
                # Áp dụng bộ lọc cho dữ liệu âm thanh
                filtered_data = self.eq_service.equalize(filtered_data)

                # Áp dụng EQ filter nếu cần
                filtered_data = np.clip(filtered_data * self.volume, -32768, 32767)

                if threshole_clip_small > 0:
                    filtered_data = self.eq_service.clip_small_amplitudes(filtered_data, threshole_clip_small)

                if self.show_graph:
                    self.notify_queued("audio_chunk_changed", {
                        "audio_data": audio_data,
                        "filtered_data": filtered_data
                    })

                # Gửi dữ liệu đã lọc đến audio stream để phát lại
                with self.lock:
                    try: 
                        self.audio_stream.write(filtered_data.astype(np.int16).tobytes())
                    except Exception as e:
                        print(f"Error writing to audio stream: {e}")
                        break

                wf.writeframes(filtered_data.astype(np.int16).tobytes())

        # Khi dừng ghi âm, xử lý cuối cùng
        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()

    def toggle_mute(self):
        if self.muted:
            self.volume = self.prev_volume  # Restore volume
        else:
            print("Volume: ", self.volume)
            self.prev_volume = self.volume  # Lưu volume hiện tại
            self.volume = 0  # Mute

        self.muted = not self.muted  # Đảo trạng thái mute

    def get_current_time(self):
        """Lấy thời gian đã phát (giây)"""
        if self.audio_stream:
            return self.audio_stream.get_position() / self.fs  # Convert frame → giây
        return 0

    def get_duration(self):
        """Lấy tổng thời lượng bài hát (giây)"""
        if self.selected_file:
            import wave
            with wave.open(self.selected_file, "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                return frames / rate
        return 0

    def process_audio_file(self, input_path):
        """
        Đọc file âm thanh, áp dụng bộ lọc equalizer và xuất file mới.

        Args:
            input_path (str): Đường dẫn file âm thanh gốc.
        """
        # Load lại config
        self.config_manager.reload_config()

        # Lấy thư mục chứa file main.py (thư mục gốc của project)
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        root_dir = os.path.abspath(os.path.join(base_dir, ".."))  

        # Tạo thư mục "FileAppliedEQ" nếu chưa tồn tại
        output_dir = os.path.join(root_dir, "FileAppliedEQ")
        os.makedirs(output_dir, exist_ok=True)

        # Lấy tên file gốc (không có đuôi)
        file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(output_dir, f"{file_name}_applied_eq.wav")

        # Đọc file WAV bằng soundfile (hỗ trợ đa kênh tốt hơn wave)
        audio_data, samplerate = sf.read(input_path, dtype='int16')

        # Nếu âm thanh là stereo (2 kênh), tách từng kênh để xử lý riêng
        if len(audio_data.shape) > 1:
            num_channels = audio_data.shape[1]  # Số kênh
            filtered_data = np.zeros_like(audio_data)

            for ch in range(num_channels):
                filtered_data[:, ch] = self.eq_service.equalize(audio_data[:, ch])

        else:
            # Xử lý âm thanh mono
            filtered_data = self.eq_service.equalize(audio_data)

        # Đảm bảo dữ liệu sau khi xử lý không bị vượt quá giới hạn int16
        filtered_data = np.clip(filtered_data, -32768, 32767).astype(np.int16)

        # Xuất file mới
        sf.write(output_path, filtered_data, samplerate)
        print(f"Processed audio saved to: {output_path}")

    # def seek_to(self, new_time):
    #     """Tua đến vị trí mới (giây)"""
    #     if not self.selected_file:
    #         print("No audio file selected!")
    #         return

    #     with self.lock:
    #         print("Seeking to:", new_time)

    #         # Tính toán vị trí frame mới
    #         new_frame = int(new_time * self.fs)  # Chuyển đổi giây → frame

    #         # Kiểm tra nếu file chưa mở hoặc bị đóng
    #         try:
    #             self.wave_file.tell()  # Kiểm tra nếu file vẫn mở
    #         except Exception:
    #             self.wave_file = wave.open(self.selected_file, 'rb')  # Mở lại file

    #         total_frames = self.wave_file.getnframes()

    #         if new_frame < total_frames:
    #             self.current_frame = new_frame
    #             self.wave_file.setpos(new_frame)  # Đặt lại vị trí đọc file

    #             # Kiểm tra xem stream có tồn tại và mở không trước khi gọi `is_active()`
    #             if self.audio_stream and hasattr(self.audio_stream, 'stream'):
    #                 try:
    #                     if self.audio_stream.stream.is_active():
    #                         self.audio_stream.stop_stream()
    #                 except OSError:
    #                     print("Stream đã bị đóng, khởi tạo lại...")  # Debug
    #                     self.audio_stream = None  # Reset lại audio_stream

    #             # Nếu stream bị đóng hoặc chưa khởi tạo, mở lại nó
    #             if self.audio_stream is None:
    #                 self.audio_stream = self.audio_stream_class(
    #                     channels=self.wave_file.getnchannels(),
    #                     rate=self.fs,
    #                     frames_per_buffer=self.config_manager.getint('general', 'audio_fpb')
    #                 )

    #             # Reset thread phát nhạc để đọc từ vị trí mới
    #             self.stopped_event.set()  # Dừng thread cũ
    #             self.stopped_event.clear()  # Cho phép thread mới chạy
    #             self._start_audio_thread(self.wave_file)  # Khởi động lại thread phát nhạc

