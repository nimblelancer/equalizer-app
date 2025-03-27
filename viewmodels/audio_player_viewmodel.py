from viewmodels.base_command import G2Command
from viewmodels.base_viewmodel import G2BaseViewModel
from models.audio_player_model import AudioPlayerModel

class AudioPlayerViewModel (G2BaseViewModel):
    def __init__(self, model: AudioPlayerModel):

        super().__init__(model)
        self.model.add_listener("player_state_changed", self)
        self.model.add_listener("audio_stream_changed", self)
        self.model.state_changed_callback = self.on_state_changed

        # Trạng thái của View
        self.is_playing = False
        self.selected_file = ""
        self.volume = 1.0

        self.play_command = G2Command(self.play_audio)
        self.stop_command = G2Command(self.stop_audio)
        self.pause_command = G2Command(self.pause_audio)
        self.unpause_command = G2Command(self.unpause_audio)
        self.voice_command = G2Command(self.voice)

    def set_update_callback(self, callback):
        """Đăng ký hàm cập nhật từ View"""
        self.update_callback = callback

    def on_state_changed(self, new_state):
        """Callback khi trạng thái thay đổi"""
        if self.update_callback:
            self.update_callback()  # Gọi View cập nhật UI

    def play_audio(self):
        """Khi nút Play được nhấn"""
        if self.model.selected_file:
            self.model.play_audio()
            self.is_playing = True

    def stop_audio(self):
        """Khi nút Stop được nhấn"""
        self.model.stop_audio()
        self.is_playing = False

    def pause_audio(self):
        """Khi nút Pause được nhấn"""
        self.model.pause_audio()
        self.is_playing = False

    def unpause_audio(self):
        """Khi nút Unpause được nhấn"""
        self.model.unpause_audio()
        self.is_playing = True

    def select_file(self, file_path):
        """Khi nút Select File được nhấn"""
        self.model.set_audio_file(file_path)

    def voice(self):
        """Khi nút Voice được nhấn"""
        self.model.start_voice()

    def setting_volume(self, value):
        """Khi nút Voice được nhấn"""
        self.model.volume = value

    def toggle_mute(self):
        """Xử lý khi click vào icon volume"""
        self.model.toggle_mute()

    def on_notify(self, event_name, data):
        if event_name == "player_state_changed":
            # Xử lý dữ liệu từ Model (tùy theo logic của bạn)
            """"""
        elif event_name == "audio_stream_changed":
            """"""
        else:
            super().notify_view(event_name, data)  # Gọi hàm super

    def get_current_time(self):
        return self.model.get_current_time()

    def get_duration(self):
        return self.model.get_duration()

    def seek_to(self, new_time):
        self.model.seek_to(new_time)
