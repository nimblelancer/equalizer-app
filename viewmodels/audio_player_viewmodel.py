from viewmodels.base_command import G2Command
from viewmodels.base_viewmodel import G2BaseViewModel
from models.audio_player_model import AudioPlayerModel

class AudioPlayerViewModel (G2BaseViewModel):
    def __init__(self, model: AudioPlayerModel):

        super().__init__(model)
        self.model.add_listener("player_changed", self)

        # self.model = model

        self.play_command = G2Command(self.play_audio)
        self.stop_command = G2Command(self.stop_audio)
        self.pause_command = G2Command(self.pause_audio)
        self.unpause_command = G2Command(self.unpause_audio)
        self.voice_command = G2Command(self.voice)

    def play_audio(self):
        """Khi nút Play được nhấn"""
        if self.model.selected_file:
            self.model.play_audio()
            # self.is_playing = True
            # self.is_paused = False
            # self.set_property("is_playing", True)

    def stop_audio(self):
        """Khi nút Stop được nhấn"""
        self.model.stop_audio()
        # self.set_property("is_playing", False)

    def pause_audio(self):
        """Khi nút Pause được nhấn"""
        self.model.pause_audio()
        # self.set_property("is_playing", False)

    def unpause_audio(self):
        """Khi nút Unpause được nhấn"""
        self.model.unpause_audio()
        # self.set_property("is_playing", True)

    def select_file(self, file_path):
        """Khi nút Select File được nhấn"""
        # self.selected_file = file_path
        self.model.set_audio_file(file_path)
        # self.set_property("selected_file", file_path)

    def voice(self):
        """Khi nút Voice được nhấn"""
        self.model.start_voice()
        # self.set_property("voice", True)

    def setting_volume(self, value):
        """Khi nút Voice được nhấn"""
        self.model.volume = value
