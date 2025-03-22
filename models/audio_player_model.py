import threading
import numpy as np
from base.base_audio_stream import G2AudioStream
from base.base_model import G2BaseModel
import wave
from core import EqualizerService
from typing import Type
import time

class AudioPlayerState:
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    RECORDING = 3

class AudioPlayerModel(G2BaseModel):
    def __init__(self, audio_stream_class: Type[G2AudioStream], eq_service: EqualizerService):
        super().__init__()

        self.state = AudioPlayerState.STOPPED
        self.audio_stream = None
        self.audio_stream_class = audio_stream_class
        self.eq_service = eq_service
        self.selected_file = None
        self.audio_thread_instance = None
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.stopped_event = threading.Event()  # Event để dừng thread

        self.volume = 1

        self.eq_apply = False
        self.notch_apply = False

        self.gains = {
            'Bass': 1,
            'Mid-bass': 1,
            'Midrange': 1,
            'Upper midrange': 1,
            'Treble': 1
        }

        self.lowcut_freq = 0
        self.highcut_freq = 0
        self.notch_low = 0
        self.notch_high = 0

        self.show_graph = False
        self.duration = 0  # Tổng thời lượng (giây)
        self.elapsed_var = 0  # Thời gian đã phát (giây)
        self.remain_var = 0  # Thời gian còn lại (giây)
        self.progress_update_active = False  # Cờ kiểm soát việc cập nhật

    def set_state(self, state):
        """Cập nhật trạng thái của audio"""
        self.state = state

    def get_state(self):
        """Lấy trạng thái hiện tại"""
        return self.state

    def _initialize_audio_info(self, wf):
        """Khởi tạo thông tin về file audio"""
        self.audio_info = {
            'framerate': wf.getframerate(),
            'nframes': wf.getnframes(),
            'nchannels': wf.getnchannels(),
            'sampwidth': wf.getsampwidth(),
            'total_frames': wf.getnframes(),
            'current_frame': 0,
            'start_time': time.time(),
            'pause_time': None,
            'total_pause_duration': 0
        }

    def play_audio(self):
        """Bắt đầu phát âm thanh từ file"""
        if not self.selected_file:
            print("No audio file selected!")
            return

        wf = wave.open(self.selected_file, 'rb')
        print("framerate:", wf.getframerate())

        # Tính toán tổng thời lượng (giây)
        self.duration = wf.getnframes() / wf.getframerate()
        self.elapsed_var = 0
        self.remain_var = self.duration
        
        # Khởi tạo thông tin audio
        self._initialize_audio_info(wf)

        self.audio_stream = self.audio_stream_class(channels=wf.getnchannels(), rate=wf.getframerate())
        self.set_state(AudioPlayerState.PLAYING)
        self.stopped_event.clear()  # Đảm bảo rằng event không bị set khi bắt đầu lại
        self._start_audio_thread(wf)
        self._start_progress_update_thread()
        
        thread_count = threading.active_count()
        print(f"Number of threads in the current process: {thread_count}")
    
    def _start_progress_update_thread(self):
        """Tạo và khởi động thread cập nhật tiến trình"""
        self.progress_update_active = True
        
        def update_progress():
            while self.get_state() == AudioPlayerState.PLAYING and not self.stopped_event.is_set() and self.progress_update_active:
                # Tính toán thời gian đã trôi qua, trừ đi thời gian tạm dừng
                elapsed_time = time.time() - self.audio_info['start_time'] - self.audio_info['total_pause_duration']
                
                # Cập nhật frame hiện tại
                self.audio_info['current_frame'] = min(
                    int(elapsed_time * self.audio_info['framerate']), 
                    self.audio_info['total_frames']
                )
                
                # Cập nhật giá trị elapsed và remain
                self.elapsed_var = elapsed_time
                self.remain_var = max(0, self.duration - elapsed_time)
                
                # Tính toán phần trăm tiến độ (0-100)
                progress_percentage = min(100, (self.audio_info['current_frame'] / self.audio_info['total_frames']) * 100)
                
                # Cập nhật UI trong luồng chính
                if hasattr(self, 'update_ui_callback') and callable(self.update_ui_callback):
                    self.update_ui_callback(progress_percentage)
                
                # Kiểm tra nếu đã kết thúc
                if self.audio_info['current_frame'] >= self.audio_info['total_frames']:
                    self.set_state(AudioPlayerState.STOPPED)
                    self.stopped_event.set()
                    if hasattr(self, 'update_ui_callback') and callable(self.update_ui_callback):
                        self.update_ui_callback(100)
                    break
                
                time.sleep(0.1)  # Cập nhật mỗi 100ms
        
        progress_thread = threading.Thread(target=update_progress)
        progress_thread.daemon = True
        progress_thread.start()

    def stop_audio(self):
        """Dừng âm thanh"""
        self.progress_update_active = False
        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()  # Set event để thông báo cho thread dừng
        if self.audio_thread_instance is not None:
            self.audio_thread_instance.join()

    def pause_audio(self):
        """Tạm dừng âm thanh"""
        if self.get_state() == AudioPlayerState.PLAYING:
            self.set_state(AudioPlayerState.PAUSED)
            if self.audio_thread_instance:
                with self.lock:
                    self.audio_stream.stop_stream()
            self.event.clear()
            
            if hasattr(self, 'audio_info'):
                self.audio_info['pause_time'] = time.time()

    def unpause_audio(self):
        """Tiếp tục phát âm thanh"""
        if self.get_state() == AudioPlayerState.PAUSED:
            self.set_state(AudioPlayerState.PLAYING)
            with self.lock:
                self.audio_stream.start_stream()
            self.event.set()
            
            if hasattr(self, 'audio_info') and self.audio_info['pause_time'] is not None:
                pause_duration = time.time() - self.audio_info['pause_time']
                self.audio_info['total_pause_duration'] += pause_duration
                self.audio_info['pause_time'] = None

    def set_progress_callback(self, callback):
        """Đặt callback để cập nhật UI từ thread khác"""
        self.update_ui_callback = callback

    # Thêm phương thức để di chuyển đến vị trí cụ thể
    def seek_to_position(self, percentage):
        """Di chuyển đến vị trí cụ thể trong file audio (0-100%)"""
        if not hasattr(self, 'audio_info') or not self.audio_info:
            return
        
        percentage = float(percentage)
        if percentage < 0:
            percentage = 0
        elif percentage > 100:
            percentage = 100
        
        # Tính toán vị trí mới (frame)
        new_frame = int((percentage / 100) * self.audio_info['total_frames'])
        
        # Cập nhật thông tin
        self.audio_info['current_frame'] = new_frame
        
        # Tính thời gian đã trôi qua mới
        elapsed = (new_frame / self.audio_info['framerate'])
        self.elapsed_var = elapsed
        self.remain_var = max(0, self.duration - elapsed)
        
        # Điều chỉnh thời gian bắt đầu để đồng bộ với vị trí mới
        current_time = time.time()
        self.audio_info['start_time'] = current_time - elapsed + self.audio_info['total_pause_duration']
        
        # Nếu đang tạm dừng, cập nhật thời gian tạm dừng
        if self.get_state() == AudioPlayerState.PAUSED:
            self.audio_info['pause_time'] = current_time

    # Thêm phương thức định dạng thời gian
    def format_time(self, seconds):
        """Format thời gian theo định dạng mm:ss"""
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f'{minutes:02}:{seconds:02}'

    def _start_audio_thread(self, wf):
        """Bắt đầu thread phát âm thanh"""
        self.audio_thread_instance = threading.Thread(target=self._audio_thread, args=(wf,))
        self.audio_thread_instance.start()

    def _audio_thread(self, wf):
        if self.state == AudioPlayerState.PAUSED:
            self.event.wait()  # Dừng thread khi paused

        chunk = 1024
        # Seek đến vị trí hiện tại nếu có
        if hasattr(self, 'audio_info') and self.audio_info['current_frame'] > 0:
            wf.setpos(self.audio_info['current_frame'])
        
        data = wf.readframes(chunk)

        while data:
            if self.get_state() != AudioPlayerState.PLAYING or self.stopped_event.is_set():
                break

            audio_data = np.frombuffer(data, dtype=np.int16)

            # Áp dụng bộ lọc cho dữ liệu âm thanh
            filtered_data = self.eq_service.equalize(audio_data, self.eq_apply, self.gains, self.lowcut_freq, self.highcut_freq, fs=44100)

            # Điều chỉnh âm lượng của dữ liệu âm thanh
            filtered_data = np.clip(filtered_data * (self.volume / 100), -32768, 32767)

            if self.show_graph:
                self.notify_queued("audio_chunk_changed", {
                    "audio_data": audio_data,
                    "filtered_data": filtered_data
                })

            with self.lock:
                if self.get_state() != AudioPlayerState.PLAYING or self.stopped_event.is_set():
                    break
                self.audio_stream.write(filtered_data.astype(np.int16).tobytes())

            data = wf.readframes(chunk)

        self.set_state(AudioPlayerState.STOPPED)
        self.stopped_event.set()
        
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